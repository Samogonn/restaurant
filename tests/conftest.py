import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.main import app, get_session

SQLALCHEMY_DATABASE_URL = "sqlite:///test_restaurant.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def get_test_session():
    db = sync_session()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
