from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.accounts.schemas import user
from db.database import get_db
from app.accounts.services.user import SQLAlchemyRepository


router = APIRouter(
    prefix='/auth'
)


@router.post('/register')
async def register(request: user.UserCreateInput, db: Session = Depends(get_db)):
    repo = SQLAlchemyRepository(db)
    return repo.create(request)