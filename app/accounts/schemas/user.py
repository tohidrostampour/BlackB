from __future__ import annotations
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


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str


class ProfileReadModel(BaseProfile):
    user_id: int

    class Config:
        orm_mode = True


class UserReadModel(BaseModel):
    id: int
    name: str
    username: str
    email: str
    profile: ProfileReadModel
    posts: list[PostReadOut]

    class Config:
        orm_mode = True


class ProfileUpdateInput(BaseProfile):
    bio: str | None = None
    age: str | None = None
    phone: str | None = None
