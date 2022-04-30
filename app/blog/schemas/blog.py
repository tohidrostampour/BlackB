import json

from pydantic import BaseModel


class BasePost(BaseModel):
    title: str
    body: str


class BaseTag(BaseModel):
    title: str


class PostCreate(BasePost):
    title: str
    body: str


class TagCreate(BaseModel):
    tags: list[BaseTag] | None = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class PostUpdate(BasePost):
    title: str | None = None
    body: str | None = None
    file: str | None = None
    tags: list[TagCreate] | None = None


class TagList(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class PostRead(BasePost):
    id: int
    owner_id: int
    title: str
    body: str
    file: str | None = None
    tags: list[TagList] | None = None

    class Config:
        orm_mode = True


class TagRead(BaseTag):
    id: int
    posts: list[PostRead] = []

    class Config:
        orm_mode = True









