from fastapi import Depends
from sqlalchemy.orm import Session

from app.blog.models.blog import Tag, Post
from app.blog.schemas import BaseTag
from db.database import get_db


class TagService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create(self, obj: list[BaseTag], post: Post):
        if obj:
            obj = obj.dict()['tags']
            for item in obj:
                tag = self.get(item.get('title')).first()

                if not self.get(item.get('title')).first():
                    tag = Tag(title=item.get('title'))

                post.tags.append(tag)
                self.session.add(tag)
                self.session.commit()
                self.session.flush()
                self.session.refresh(tag)

    def get(self, title: str):
        return self.session.query(Tag).filter(Tag.title == title)

    def list(self):
        return self.session.query(Tag).all()

    def list_posts(self, id: int):
        return self.session.query(Tag).filter(Tag.id == id).first()
