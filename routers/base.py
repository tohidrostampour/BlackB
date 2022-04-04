from fastapi import APIRouter

from routers.blog import posts, tags
from routers.accounts import auth, dashboard, users


api_router = APIRouter()

api_router.include_router(auth.router, tags=['auth'])
api_router.include_router(users.router, tags=['users'])
api_router.include_router(dashboard.router, tags=['dashboard'])
api_router.include_router(posts.router, tags=['posts'])
api_router.include_router(tags.router, tags=['tags'])

