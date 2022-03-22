from fastapi import APIRouter, Depends, status

from app.accounts.schemas import user
from app.accounts.services.user_service import UserService

router = APIRouter(
    prefix='/auth'
)


@router.post('/register', response_model=user.UserReadModel, status_code=status.HTTP_201_CREATED)
async def register(request: user.UserCreateInput, service: UserService = Depends(UserService)):
    return service.create(request)


