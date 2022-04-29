import datetime

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.hashing import Hash
from db.base import Base
from app.accounts.schemas import UserCreate, UserUpdate, ProfileUpdate


class User(Base):


    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    posts = relationship('Post', back_populates='owner',
                         cascade="all, delete",
                         passive_deletes=True)
    comments = relationship('Comment', back_populates='comment_owner',
                            cascade="all, delete",
                            passive_deletes=True
                            )
    profile = relationship('Profile', back_populates='user', uselist=False,
                           cascade="all, delete",
                           passive_deletes=True
                           )

    def __init__(self, inp: UserCreate):
        self.name = inp.name
        self.username = inp.username
        self.email = inp.email
        self.password = Hash.bcrypt(inp.password)

    def update(self, inp: UserUpdate):
        self.name = inp.name
        self.username = inp.username
        self.email = inp.email
        self.updated_at = datetime.datetime.now()


class Profile(Base):

    id = Column(Integer, primary_key=True, autoincrement=True)
    bio = Column(String, nullable=True)
    age = Column(Integer, nullable=True)
    phone = Column(String, nullable=True)
    user = relationship('User', back_populates='profile')
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))

    def __init__(self, user_id):
        self.user_id = user_id

    def update(self, inp: ProfileUpdate):
        self.bio = inp.bio
        self.age = inp.age
        self.phone = inp.phone
        self.updated_at = datetime.datetime.now()