from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    owner = relationship('User', back_populates='posts')
    owner_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String, unique=True)
    body = Column(String)
    file = Column(String)
    comments = relationship('Comment', back_populates='post')
    tags = relationship('Tag', back_populates='post')


class Comment(Base):
    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)
    comment_owner = relationship('User', back_populates='comments')
    owner_id = Column(Integer, ForeignKey('user.id'))
    post = relationship('Post', back_populates='comments')
    post_id = Column(Integer, ForeignKey('post.id'))


class Tag(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    post = relationship('Post', back_populates='tags')
    post_id = Column(Integer, ForeignKey('post.id'))
