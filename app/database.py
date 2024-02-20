from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///restaurant.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

sync_sesion = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
