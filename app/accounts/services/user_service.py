from datetime import datetime

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import exc

from app.accounts.models import User
from app.accounts.schemas import UserCreate, UserPasswordUpdate, UserUpdate
from app.accounts.services.profile_service import ProfileService
from core.hashing import Hash
from db.database import get_db
from lib.errors import NotFoundException


class UserService:
    def __init__(self, session: Session = Depends(get_db), profile_service: ProfileService = Depends(ProfileService)):
        self.session = session
        self.profile_service = profile_service

    def create(self, user_input: UserCreate):
        user = User(user_input)
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
        user: User = self.get_or_not_found(pk)
        self.session.delete(user)
        self.session.commit()

    def get_all_posts(self, pk: int):
        return self.session.query(User). \
            filter(User.id == pk) \
            .filter(User.is_active == True) \
            .options(joinedload(User.posts), joinedload(User.profile)).first()

    def update_password(self, obj: UserPasswordUpdate, user_id: int):
        user: User = self.session.query(User).filter(User.id == user_id).first()
        if not Hash.verify(obj.current_password, user.password):
            raise HTTPException(
                detail="Password is wrong, try again!",
                status_code=status.HTTP_401_UNAUTHORIZED
            )

        user.password = Hash.bcrypt(obj.new_password)
        self.session.commit()
        self.session.refresh(user)

        return user

    def update_credentials(self, user_input: UserUpdate, user_id: int):

        user: User = self.session.query(User).filter(User.id == user_id).first()
        user.update(user_input)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_email(self, email: str):
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str):
        return self.session.query(User).filter(User.username == username).first()

    def authenticate_user(self, username: str, password: str):
        user = self.get_user_by_username(username)

        if not user:
            return
        if not Hash.verify(password, user.password):
            return

        return user

    def get_or_not_found(self, id: int) -> User:
        user: User = self.session.query(User).filter(User.id == id).first()
        if user:
            return user
        else:
            raise NotFoundException(f"user with id {id} not found")
