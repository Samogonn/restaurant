from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import engine, sync_session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def start():
    uvicorn.run("app.main:app", reload=True)


# Dependency
def get_session():
    db = sync_session()
    try:
        yield db
    finally:
        db.close()


@app.get("/menu/{id}")
def get_menu(id: int, session: Session = Depends(get_session)):
    db_menu = crud.menu_crud.get(id, session)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return db_menu


@app.get("/menu")
def get_all_menus(session: Session = Depends(get_session)):
    return crud.menu_crud.get_all(session)


@app.post("/menu", status_code=status.HTTP_201_CREATED)
def add_menu(
    menu: Annotated[schemas.MenuCreate, Depends()],
    session: Session = Depends(get_session),
):
    db_menu = crud.menu_crud.add(menu, session)
    return db_menu


@app.patch("/menu/{id}")
def update_menu(
    id: int,
    menu: Annotated[schemas.MenuUpdate, Depends()],
    session: Session = Depends(get_session),
):
    db_menu = crud.menu_crud.get(id, session)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_menu = crud.menu_crud.update(db_menu, menu, session)
    return db_menu


@app.delete("/menu/{id}")
def remove_menu(id: int, session: Session = Depends(get_session)):
    db_menu = crud.menu_crud.get(id, session)
    if db_menu is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_menu = crud.menu_crud.remove(id, session)
    return db_menu
