from __future__ import annotations
from pydantic import BaseModel, EmailStr

from app.accounts.schemas import ProfileRead
from app.blog.schemas import PostRead


class BaseUser(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class UserCreate(BaseUser):
    pass


class UserUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    email: EmailStr | None = None


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str


class UserRead(BaseModel):
    id: int
    name: str
    username: str
    email: str
    profile: ProfileRead = None
    posts: list[PostRead]

    class Config:
        orm_mode = True

