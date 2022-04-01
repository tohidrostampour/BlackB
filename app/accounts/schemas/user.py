from pydantic import BaseModel, EmailStr

from app.blog.schemas import PostReadOut


class BaseUser(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class BaseProfile(BaseModel):
    bio: str
    age: int
    phone: str


class UserCreateInput(BaseUser):
    pass


class UserUpdateInput(BaseUser):
    id: int


class UserReadModel(BaseModel):
    id: int
    name: str
    username: str
    email: str
    posts: list[PostReadOut]

    class Config:
        orm_mode = True


class ProfileUpdateInput(BaseProfile):
    id: int


class ProfileReadModel(BaseProfile):
    id: int

    class Config:
        orm_mode = True
