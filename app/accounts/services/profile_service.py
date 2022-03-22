from typing import Any

from fastapi import Depends
from sqlalchemy.orm import Session

from app.accounts.models import Profile
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

    def get_all(self, pk: Any):
        return self.session.query(Profile).all()

    def update(self, pk):
        pass

    def destroy(self, pk):
        profile = self.session.query(Profile).filter(id=pk)
        if profile:
            self.session.delete(profile)
        return 'Not found'
