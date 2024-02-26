import abc

from sqlalchemy.orm import Session

from app import models, schemas


class AbstractCRUD[T](abc.ABC):
    @abc.abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, id: int) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, id: int, **kwargs: object) -> None:
        raise NotImplementedError


class SqlAlchemyMenuCRUD(AbstractCRUD[models.Menu]):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, menu: schemas.MenuCreate):
        db_menu = models.Menu(name=menu.name, description=menu.description)
        self.session.add(db_menu)
        self.session.commit()
        self.session.refresh(db_menu)
        return db_menu

    def get(self, id: int):
        db_menu = (
            self.session.query(models.Menu)
            .filter(models.Menu.id == id)
            .first()
        )
        return db_menu

    def get_all(self):
        all_menus = self.session.query(models.Menu).all()
        return all_menus

    def remove(self, menu: schemas.MenuDB):
        self.session.delete(menu)
        self.session.commit()
        return menu

    def update(self, id: int, menu: schemas.MenuUpdate):
        menu_query = self.session.query(models.Menu).filter(
            models.Menu.id == id
        )
        db_menu = menu_query.first()
        menu_query.update(menu.model_dump())
        self.session.commit()
        self.session.refresh(db_menu)
        return db_menu


class MockMenuCRUD(AbstractCRUD[models.Menu]):
    def __init__(self, menus: dict[int, schemas.MenuBase] | None) -> None:
        self.menus = menus or {}

    def get(self, id: int):
        return self.menus[id]

    def get_all(self) -> list[models.Menu]:
        return list(self.menus.values())

    def add(self, menu: schemas.MenuCreate) -> None:
        self.menus[len(self.menus)] = menu

    def update(self, id: int, menu: schemas.MenuUpdate) -> None:
        self.menus[id] = menu
