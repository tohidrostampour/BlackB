from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, Table
from sqlalchemy.orm import relationship, backref
from db.base import Base


class Post(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)
    body = Column(String)
    file = Column(String)

    owner = relationship('User', back_populates='posts')
    owner_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))

    comments = relationship('Comment', back_populates='post',
                            cascade="all, delete",
                            passive_deletes=True)

    tags = relationship('Tag', secondary='post_tag',
                        back_populates='posts',
                        cascade="all, delete"
                       )


class Comment(Base):
    def __init__(self, body, owner_id, post_id, comment_id=None):
        self.comment_id = comment_id
        self.post_id = post_id
        self.owner_id = owner_id
        self.body = body

    id = Column(Integer, primary_key=True, index=True)
    body = Column(String)

    comment_owner = relationship('User', back_populates='comments', )
    owner_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))

    post = relationship('Post', back_populates='comments')
    post_id = Column(Integer, ForeignKey('post.id', ondelete="CASCADE"))

    comment_id = Column(Integer, ForeignKey('comment.id', ondelete="CASCADE"), nullable=True)
    reply = relationship("Comment", remote_side=[id], backref=backref('replies'), uselist=False,
                         cascade="all, delete",
                         passive_deletes=True)


class Tag(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True)

    posts = relationship('Post', secondary='post_tag', back_populates='tags',  passive_deletes='all')


post_tag = Table('post_tag', Base.metadata,
                 Column('tag_id', Integer, ForeignKey('tag.id', ondelete="CASCADE")),
                 Column('post_id', Integer, ForeignKey('post.id', ondelete="CASCADE"))
                 )
