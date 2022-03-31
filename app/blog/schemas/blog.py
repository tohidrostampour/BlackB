from __future__ import annotations

import datetime
import json

from fastapi import Form
from pydantic import BaseModel, AnyUrl


class BasePost(BaseModel):
    title: str
    body: str


class BaseComment(BaseModel):
    body: str


class BaseTag(BaseModel):
    title: str


class CommentCreateIn(BaseComment):
    pass


class CommentReadOut(BaseComment):
    owner_id: int
    comment_id: int | None = None
    id: int

    class Config:
        orm_mode = True


class CommentUpdateIn(BaseComment):
    pass


class Tag(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class TagCreateIn(BaseModel):
    tags: list[BaseTag] | None = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class PostCreateIn(BasePost):
    title: str
    body: str


class PostReadOut(BasePost):
    id: int
    title: str
    body: str
    file: str | None = None

    class Config:
        orm_mode = True


class PostsInTagOut(BasePost):
    id: int
    title: str
    body: str
    file: str | None = None

    class Config:
        orm_mode = True


class TagReadOut(BaseTag):
    id: int
    posts: list[PostsInTagOut] = []

    class Config:
        orm_mode = True


class PostUpdateIn(BasePost):
    title: str | None = None
    body: str | None = None
    file: str | None = None
    tags: list[TagCreateIn] | None = None
