from fastapi import Depends
from sqlalchemy.orm import Session

from app.blog.models.blog import Post
from app.blog.schemas import PostCreateIn
from db.database import get_db


class PostService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create(self, post: PostCreateIn, owner_id):
        post = Post(
            title=post.title,
            body=post.body,
            file=post.file,
            owner_id=owner_id)
        self.session.add(post)
        self.session.commit()
        self.session.flush()
        self.session.refresh(post)
        return post

    def list(self):
        return self.session.query(Post).all()

    def get(self, id):
        return self.session.query(Post).filter(Post.id == id).first()