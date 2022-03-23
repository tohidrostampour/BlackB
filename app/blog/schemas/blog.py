from __future__ import annotations
from pydantic import BaseModel, AnyUrl


class BasePost(BaseModel):
    title: str
    body: str
    file: AnyUrl


class BaseComment(BaseModel):
    body: str


class BaseTag(BaseModel):
    title: str


class PostCreateIn(BasePost):
    title: str
    body: str
    file: AnyUrl


class PostReadOut(BasePost):
    id: int
    title: str
    body: str
    file: AnyUrl

    class Config:
        orm_mode = True


class PostUpdateIn(BasePost):
    tags: list[TagReadOut]


class CommentCreateIn(BaseComment):
    post_id: int


class CommentReadOut(BaseComment):
    post_id: int


class CommentUpdateIn(BaseComment):
    pass


class TagCreateIn(BaseTag):
    post_id: int


class TagReadOut(BaseComment):
    post_id: int

