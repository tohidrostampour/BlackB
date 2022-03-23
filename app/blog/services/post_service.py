from fastapi import Depends
from sqlalchemy.orm import Session

from app.blog.models.blog import Post
from app.blog.schemas import PostCreateIn, PostUpdateIn
from db.database import get_db


class PostService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create(self, post: PostCreateIn, owner_id: int):
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

    def get(self, id: int):
        return self.session.query(Post).filter(Post.id == id).first()

    def put(self, id: int, post: PostCreateIn, owner_id: int):
        existing_post = self.session.query(Post).filter(Post.id == id)
        if not existing_post.first():
            return
        post.__dict__.update(owner_id=owner_id)
        existing_post.update(post.__dict__)
        self.session.commit()
        return True

    def destroy(self, id: int, owner_id: int):
        existing_post = self.session.query(Post).filter(Post.id == id)
        if not existing_post.first():
            return
        existing_post.delete(synchronize_session=False)
        self.session.commit()
        return True
