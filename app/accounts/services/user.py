
from sqlalchemy.orm import Session

from app.accounts.schemas.user import UserCreateInput
from app.accounts.models.user import User

from .hashing import Hash


def create(request: UserCreateInput, db: Session):
    new_user = User(
        username=request.username,
        name=request.name,
        email=request.email,
        password=Hash().bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.flush()
    db.refresh(new_user)
    return new_user
