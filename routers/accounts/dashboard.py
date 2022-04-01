from fastapi import APIRouter, Depends

from app.accounts.schemas import UserReadModel
from app.accounts.services import UserService

router = APIRouter(
    prefix='/dashboard'
)


@router.get('/{user_id}', response_model=UserReadModel)
async def get_user_posts(user_id: int, service: UserService = Depends(UserService)):
    # current_user_id = 1
    return service.get_all_posts(pk=user_id)
