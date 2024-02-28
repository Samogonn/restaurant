import abc

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


class AbstractCRUD[T](abc.ABC):
    @abc.abstractmethod
    def get(self, id: int) -> T:
        raise NotImplementedError

    @abc.abstractmethod
    def get_all(self) -> list[T]:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, **kwargs: object) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def update(self, id: int, **kwargs: object) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, id: int) -> None:
        raise NotImplementedError


class SqlAlchemyCRUDBase(AbstractCRUD):
    """
    Main CRUD
    """

    def __init__(self, model) -> None:
        self.model = model

    def get(self, id: int, session: Session):
        db_obj = (
            session.execute(select(self.model).where(self.model.id == id))
            .scalars()
            .first()
        )
        return db_obj

    def get_all(self, session: Session):
        all_objs = session.execute(select(self.model)).scalars().all()
        return all_objs

    def add(self, obj_in, session: Session):
        obj_in = obj_in.model_dump()
        db_obj = self.model(**obj_in)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(self, db_obj, obj_in, session: Session):
        obj_data = jsonable_encoder(db_obj)

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def remove(self, id: int, session: Session):
        db_obj = (
            session.execute(select(self.model).where(self.model.id == id))
            .scalars()
            .first()
        )
        session.delete(db_obj)
        session.commit()
        return db_obj


class SqlAlchemyMenuCRUD(AbstractCRUD[models.Menu]):
    """
    CRUD for practice
    """

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


menu_crud = SqlAlchemyCRUDBase(models.Menu)
