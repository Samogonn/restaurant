from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app import schemas, models
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
    db_menu = session.query(models.Menu).filter(models.Menu.id == id).first()
    return db_menu


@app.post("/menu")
def add_menu(menu: schemas.MenuCreate, session: Session = Depends(get_session)):
    db_menu = models.Menu(name=menu.name, description=menu.description)
    session.add(db_menu)
    session.commit()
    session.refresh(db_menu)
    return db_menu
