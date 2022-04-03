from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from app.accounts.schemas import UserCreateInput, UserPasswordUpdate
from app.accounts.models import User
from app.accounts.services.profile_service import ProfileService
from core.hashing import Hash
from db.database import get_db


class UserService:
    def __init__(self, session: Session = Depends(get_db), profile_service: ProfileService = Depends(ProfileService)):
        self.session = session
        self.profile_service = profile_service

    def create(self, obj: UserCreateInput):
        user = User(
            name=obj.name,
            username=obj.username,
            email=obj.email,
            password=Hash.bcrypt(obj.password)
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        self.profile_service.create(user.id)
        return user

    def get_all(self):
        return self.session.query(User).all()

    def update(self, pk):
        pass

    def destroy(self, pk):
        user = self.session.query(User).filter(id=pk)
        if user:
            self.session.delete(user)
        return 'Not found'

    def get_all_posts(self, pk: int):
        return self.session.query(User).\
            filter(User.id == pk)\
            .filter(User.is_active == True)\
            .options(joinedload(User.posts), joinedload(User.profile)).first()

    def update_password(self, obj: UserPasswordUpdate, user_id: int):
        user = self.session.query(User).filter(User.id == user_id).first()
        if not Hash.verify(obj.current_password, user.password):
            return
        user.password = Hash.bcrypt(obj.new_password)
        self.session.commit()
        self.session.refresh(user)

        return True
