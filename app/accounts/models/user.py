from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base


class User(Base):
    def __init__(self, name, username, email, password):
        self.password = password
        self.email = email
        self.username = username
        self.name = name

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    posts = relationship('Post', back_populates='owner')
    comments = relationship('Comment', back_populates='comment_owner')
    profile = relationship('Profile', back_populates='user', uselist=False)


class Profile(Base):
    def __init__(self, user_id):
        self.user_id = user_id

    id = Column(Integer, primary_key=True, autoincrement=True)
    bio = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    phone = Column(String, nullable=True)
    user = relationship('User', back_populates='profile')
    user_id = Column(Integer, ForeignKey('user.id'))
