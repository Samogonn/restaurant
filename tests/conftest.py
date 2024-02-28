import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models
from app.database import Base
from app.main import app, get_session

SQLALCHEMY_DATABASE_URL = "sqlite:///test_restaurant.db"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

sync_testing_session = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine
)


def override_get_db():
    db = sync_testing_session()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(autouse=True, scope="module")
def prepare_db():
    Base.metadata.create_all(bind=test_engine)
    session = sync_testing_session()
    menus = [models.Menu(**obj) for obj in test_db_data]
    session.add_all(menus)
    session.commit()
    yield
    Base.metadata.drop_all(bind=test_engine)


test_db_data = [
    {"description": "Delicious pizza!", "name": "Best Pizza"},
    {"description": "Family restaurant", "name": "Papa's Burgers"},
]
