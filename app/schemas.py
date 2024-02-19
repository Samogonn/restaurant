from pydantic import BaseModel


class MenuBase(BaseModel):
    name: str
    description: str | None = None


class MenuCreate(MenuBase):
    pass


class DBMenu(BaseModel):
    id: int
