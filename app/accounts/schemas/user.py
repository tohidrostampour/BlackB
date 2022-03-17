from pydantic import BaseModel


class BaseUser(BaseModel):
    name: str
    username: str
    email: str
    password: str


class UserCreateInput(BaseUser):
    pass


class UserUpdateInput(BaseUser):

    id: int
    info: str


class UserReadModel(BaseUser):
    id: int

    class Config:
        orm_mode = True
