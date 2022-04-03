from pydantic import BaseModel


class BaseComment(BaseModel):
    body: str


class CommentCreate(BaseComment):
    pass


class CommentRead(BaseComment):
    owner_id: int
    comment_id: int | None = None
    id: int

    class Config:
        orm_mode = True


class CommentUpdate(BaseComment):
    pass
