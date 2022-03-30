from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy.orm import Session

from app.blog.models.blog import Post, Comment
from app.blog.schemas import PostCreateIn, PostUpdateIn
from db.database import get_db


class PostService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create(self, obj: dict, owner_id: int, url: str):
        post = Post(
            title=obj['title'],
            body=obj['body'],
            file=str(url),
            owner_id=owner_id)
        self.session.add(post)
        self.session.commit()
        self.session.flush()
        self.session.refresh(post)
        return post

    def list(self):
        return self.session.query(Post).all()

    def get(self, id: int):
        return self.session.query(Post).filter(Post.id == id).first()

    def put(self, id: int, post: PostCreateIn, owner_id: int):
        existing_post = self.session.query(Post).filter(Post.id == id)
        if not existing_post.first():
            return
        post.__dict__.update(owner_id=owner_id)
        post.__dict__.update(updated_at=datetime.now(timezone.utc))
        existing_post.update(post.__dict__)
        self.session.commit()
        return True

    def destroy(self, id: int, owner_id: int):
        existing_post = self.session.query(Post).filter(Post.id == id)
        if not existing_post.first():
            return
        existing_post.delete()
        self.session.flush()
        self.session.commit()
        return True

    def list_comments(self, post_id):
        comments = self.session.query(Comment).filter(Comment.post_id == post_id).all()
        result = []
        for comment in comments:
            if not comment.comment_id:
                result.append(comment)

            type(comment.replies)  # TODO: Why it doesn't show replies without using comment.replies in code???

        return result
