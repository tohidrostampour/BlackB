from datetime import datetime
from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session, joinedload

from app.accounts.models import Profile
from app.accounts.schemas import ProfileUpdateInput
from db.database import get_db


class ProfileService:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def create(self, user_id):
        profile = Profile(user_id=user_id)
        self.session.add(profile)
        self.session.commit()
        self.session.refresh(profile)
        return profile

    def get(self, pk):
        return self.session.query(Profile).filter(Profile.user_id == pk).first()

    def get_all(self, pk: Any):
        return self.session.query(Profile).all()

    def destroy(self, pk):
        profile = self.session.query(Profile).filter(id=pk)
        if profile:
            self.session.delete(profile)
        return 'Not found'

    def put(self, obj: ProfileUpdateInput, user_id: int):
        existing_prf = self.session.query(Profile).filter(Profile.user_id == user_id)
        if not existing_prf.first():
            return
        obj.__dict__.update(user_id=user_id)
        obj.__dict__.update(updated_at=datetime.now())
        existing_prf.update(obj.dict(exclude_defaults=True, exclude_none=True))
        self.session.commit()
        return True
