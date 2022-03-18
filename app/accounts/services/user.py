from abc import ABC

from sqlalchemy.orm import Session

from app.accounts.schemas.user import UserCreateInput
from app.accounts.models.user import User
from core.hashing import Hash
from app.accounts.services.repository import AbstractRepository


class SQLAlchemyRepository(AbstractRepository):
    def __init__(self, session: Session):
        self.session = session

    def get(self, pk):
        return self.session.query(User).get(id=pk)

    def create(self, request: UserCreateInput):
        new_user = User(
            username=request.username,
            name=request.name,
            email=request.email,
            password=Hash().bcrypt(request.password)
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.flush()
        self.session.refresh(new_user)
        return new_user

    def delete(self, pk):
        obj = self.get(pk)
        self.session.delete(obj)
        self.session.commit()


class FakeRepository(AbstractRepository):
    def __init__(self, users):
        self.session = list(users)

    def get(self, pk):
        return next(usr for usr in self.session if usr.id == pk)

    def create(self, request: User):
        new_user = User(
            username=request.username,
            name=request.name,
            email=request.email,
            password=Hash().bcrypt(request.password)
        )
        self.session.append(new_user)
        return new_user

    def delete(self, pk):
        obj = self.get(pk)
        self.session.remove(obj)
        return 'deleted successfully'

    def list(self):
        return [user for user in self.session]
