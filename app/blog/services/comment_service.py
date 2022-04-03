from fastapi import Depends
from sqlalchemy.orm import Session

from app.blog.models.blog import Comment
from app.blog.schemas import CommentCreate
from db.database import get_db


class CommentService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create(self, obj: CommentCreate, owner_id: int, post_id: int, comment_id: int | None = None):
        if comment_id:
            comment = Comment(
                body=obj.body,
                owner_id=owner_id,
                post_id=post_id,
                comment_id=comment_id
            )
        else:
            comment = Comment(
                body=obj.body,
                owner_id=owner_id,
                post_id=post_id,
            )
        self.session.add(comment)
        self.session.commit()
        self.session.flush()
        self.session.refresh(comment)
        return comment

    def list(self, post_id):
        comments = self.session.query(Comment).filter(Comment.post_id == post_id).all()
        result = {}
        for comment in comments:
            result[comment.id] = comment

            type(comment.replies)  # TODO: Why it doesn't show replies without using comment.replies in code???

        return result

    def get(self, id):
        return self.session.query(Comment).filter(Comment.id == id)
