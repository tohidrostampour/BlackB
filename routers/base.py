from fastapi import APIRouter

from routers.blog import posts, tags
from routers.accounts import auth


api_router = APIRouter()

api_router.include_router(posts.router, tags=['posts'])
api_router.include_router(auth.router, tags=['auth'])
api_router.include_router(tags.router, tags=['tags'])