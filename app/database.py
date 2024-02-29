from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///restaurant.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

sync_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    def __repr__(self):

        cols = []

        for key in self.__table__.columns.keys():
            cols.append(f"{key}: {getattr(self, key)}")

        return f"{self.__class__.__name__}({', '.join(cols)})"
