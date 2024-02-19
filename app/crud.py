import abc
from app import models
from sqlalchemy.orm import Session


class AbstractCRUD(abc.ABC):
    @abc.abstractmethod
    def add(self, menu: models.Menu):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int):
        raise NotImplementedError


class SqlAlchemyCRUD(AbstractCRUD):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, menu):
        db_menu = models.Menu(name=menu.name, description=menu.description)
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        return db_menu

    def get(self, id):
        db_menu = self.session.query(models.Menu).filter(models.Menu.id == id).first()
        return db_menu

    def get_all(self):
        all_menus = self.session.query(models.Menu).all()
        return all_menus
