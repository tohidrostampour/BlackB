from fastapi import APIRouter, Depends, HTTPException, status

from app.accounts.models import User
from app.accounts.services import ProfileService, UserService
from app.accounts.schemas import ProfileUpdate, ProfileRead, UserPasswordUpdate, UserUpdate, UserRead
from core.security import get_current_active_user

router = APIRouter(
    prefix='/users'
)


@router.get('/{user_id}', response_model=ProfileRead)
async def get_user_profile(user_id: int,
                           service: ProfileService = Depends(ProfileService),
                           current_user: User = Depends(get_current_active_user)):

    current_user_id = current_user.id
    if not user_id == current_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Permission Denied!")
    profile = service.get(user_id)
    return profile


@router.patch('/profile')
async def update_user_profile(request: ProfileUpdate,
                              service: ProfileService = Depends(ProfileService),
                              current_user: User = Depends(get_current_active_user)):

    current_user_id = current_user.id
    profile_update = service.put(request, current_user_id)
    if not profile_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Bad request, Try again!")
    return {'msg': 'Profile updated successfully!'}


@router.post('/update-password')
async def update_password(request: UserPasswordUpdate,
                          service: UserService = Depends(UserService),
                          current_user: User = Depends(get_current_active_user)):

    current_user_id = current_user.id
    if not service.update_password(request, current_user_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Current password didn\'t match')
    return {'msg': 'Password updated successfully!'}


@router.patch('/credentials')
async def update_credentials(request: UserUpdate,
                             service: UserService = Depends(UserService),
                             current_user: User = Depends(get_current_active_user)):

    current_user_id = current_user.id
    user_update = service.update_credentials(request, current_user_id)
    if not user_update:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with that email or username exists, Try again!')
    return {'msg': 'Updated successfully'}
