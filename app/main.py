from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel


app = FastAPI()


class Menu(BaseModel):
    restaurant_name: str
    description: str | None = None


class DBMenu(Menu):
    id: int


class MenuCreate(Menu):
    pass


menus = []


@app.get("/menu")
def get_menu():
    menu = Menu(restaurant_name="Papa Burgers", description="Family Restaurant")
    return menu


@app.post("/menu")
def add_menu(menu: Annotated[MenuCreate, Depends()]):
    menus.append(menu)
    return {"status": "ok"}
