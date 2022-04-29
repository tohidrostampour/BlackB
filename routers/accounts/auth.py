from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.accounts.schemas import UserRead, UserCreate, Token
from app.accounts.services.user_service import UserService
from core.config import settings
from core.security import create_access_token

router = APIRouter(
    prefix='/auth'
)


@router.post('/token', response_model=Token)
async def token(request: OAuth2PasswordRequestForm = Depends(), service: UserService = Depends(UserService)):
    user = service.authenticate_user(request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "user_id": user.id, "token_type": "bearer"}


@router.post('/register', response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(request: UserCreate, service: UserService = Depends(UserService)):
    if not request:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please try again with correct data!"
        )
    return service.create(request)
