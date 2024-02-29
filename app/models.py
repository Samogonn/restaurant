from typing import Annotated

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

# Mapped attribute
intpk = Annotated[int, mapped_column(primary_key=True)]
name = Annotated[str, mapped_column(String(64), nullable=False)]


class Menu(Base):
    __tablename__ = "menus"

    id: Mapped[intpk]
    name: Mapped[name]
    description: Mapped[str]


class SubMenu(Base):
    __tablename__ = "submenus"

    id: Mapped[intpk]
    name: Mapped[name]
    description: Mapped[str]

    menu_id: Mapped[int] = mapped_column(
        ForeignKey("menus.id", ondelete="CASCADE")
    )


class Dish(Base):
    __tablename__ = "dishes"

    id: Mapped[intpk]
    name: Mapped[name]
    description: Mapped[str]

    menu_id: Mapped[int] = mapped_column(
        ForeignKey("menus.id", ondelete="CASCADE")
    )
