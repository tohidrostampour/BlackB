from datetime import datetime
from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from app.accounts.models import Profile
from app.accounts.schemas import ProfileUpdate
from db.database import get_db
from lib.errors import NotFoundException


class ProfileService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create(self, user_id):
        profile = Profile(user_id=user_id)
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)
        return profile

    def get(self, pk: int):
        return self.get_or_not_found(pk)

    def get_all(self, pk: Any):
        return self.session.query(Profile).all()

    def destroy(self, pk):
        profile: Profile = self.get_or_not_found(pk)
        if profile:
            self.session.delete(profile)

    def put(self, profile_input: ProfileUpdate, user_id: int):
        profile: Profile = self.session.query(Profile).filter(Profile.user_id == user_id).first()
        profile.update(profile_input)
        self.session.commit()
        self.session.refresh(profile)
        return profile

    def get_or_not_found(self, id: int) -> Profile:
        profile: Profile = self.session.query(Profile).filter(Profile.user_id == id).first()

        if profile:
            return profile
        else:
            raise NotFoundException(f"user with id {id} not found")
