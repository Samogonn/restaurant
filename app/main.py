from typing import Annotated
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.database import sync_sesion, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_session():
    db = sync_sesion()
    try:
        yield db
    finally:
        db.close()


@app.get("/menu/{id}")
def get_menu(id: int, session: Session = Depends(get_session)):
    db_menu = crud.SqlAlchemyCRUD(session).get(id)
    return db_menu


@app.get("/menu")
def get_all_menus(session: Session = Depends(get_session)):
    return crud.SqlAlchemyCRUD(session).get_all()


@app.post("/menu")
def add_menu(menu: Annotated[schemas.MenuCreate, Depends()], session: Session = Depends(get_session)):
    db_menu = crud.SqlAlchemyCRUD(session).add(menu)
    return db_menu


@app.patch("/menu/{id}")
def update_menu(id: int, menu: schemas.MenuUpdate, session: Session = Depends(get_session)):
    db_menu = crud.SqlAlchemyCRUD(session).update(id, menu)
    return db_menu


@app.delete("/menu/{id}")
def remove_menu(id: int, session: Session = Depends(get_session)):
    db_menu = crud.SqlAlchemyCRUD(session).get(id)
    db_menu = crud.SqlAlchemyCRUD(session).remove(db_menu)
    return db_menu
