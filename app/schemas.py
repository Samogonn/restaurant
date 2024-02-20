from pydantic import BaseModel


class MenuBase(BaseModel):
    name: str
    description: str | None = None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    name: str | None


class MenuDB(BaseModel):
    id: int
