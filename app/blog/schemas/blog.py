from __future__ import annotations

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


class PostCreateIn(BasePost):
    title: str
    body: str


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


class TagCreateIn(BaseModel):
    tags: list[BaseTag]

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class Tag(BaseTag):
    class Config:
        orm_mode = True


class PostReadOut(BasePost):
    id: int
    title: str
    body: str
    file: str | None = None
    tags: list[Tag] = []

    class Config:
        orm_mode = True


class TagReadOut(BaseTag):
    posts: list[PostReadOut] = []

    class Config:
        orm_mode = True


class PostUpdateIn(BasePost):
    tags: list[TagReadOut]
