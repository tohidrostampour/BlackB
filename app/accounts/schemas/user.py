from __future__ import annotations

import datetime

from pydantic import BaseModel, EmailStr

from app.blog.schemas import PostRead


class BaseUser(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str


class BaseProfile(BaseModel):
    bio: str | None = None
    age: int | None = None
    phone: str | None = None


class ProfileRead(BaseProfile):
    user_id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        orm_mode = True


class ProfileUpdate(BaseProfile):
    bio: str | None = None
    age: str | None = None
    phone: str | None = None


class UserCreate(BaseUser):
    pass


class UserUpdate(BaseModel):
    name: str | None = None
    username: str | None = None
    email: EmailStr | None = None

    class Config:
        orm_mode = True


class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str


class UserRead(BaseModel):
    id: int
    name: str
    username: str
    email: str
    is_active: bool
    profile: ProfileRead = None
    posts: list[PostRead]

    class Config:
        orm_mode = True
