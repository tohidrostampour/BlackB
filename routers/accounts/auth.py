from fastapi import APIRouter, Depends, status

from app.accounts.schemas import UserReadModel, UserCreateInput
from app.accounts.services.user_service import UserService

router = APIRouter(
    prefix='/auth'
)


@router.post('/register', response_model=UserReadModel, status_code=status.HTTP_201_CREATED)
async def register(request: UserCreateInput, service: UserService = Depends(UserService)):
    return service.create(request)


