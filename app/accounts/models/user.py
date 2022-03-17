from sqlalchemy import Column, Integer, String

from db.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    info = Column(String, nullable=True)
    password = Column(String)
