from fastapi import APIRouter, Depends, HTTPException, status

from app.accounts.services import ProfileService
from app.accounts.schemas import ProfileUpdateInput, ProfileReadModel

router = APIRouter(
    prefix='/users'
)


@router.get('/{user_id}', response_model=ProfileReadModel)
async def get_user_profile(user_id: int, service: ProfileService = Depends(ProfileService)):
    current_user_id = 1
    if not user_id == current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied!")

    profile = service.get(user_id)

    return profile


@router.patch('/{user_id}/profile')
async def update_user_profile(user_id: int, request: ProfileUpdateInput,
                              service: ProfileService = Depends(ProfileService)):
    current_user_id = 1
    if not user_id == current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied!")
    profile_update = service.put(request, current_user_id)
    if not profile_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request, Try again!")

    return {'msg': 'Profile updated successfully!'}


