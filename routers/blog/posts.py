from fastapi import APIRouter, Depends, status, HTTPException

from app.blog.schemas import PostReadOut, PostCreateIn
from app.blog.services import PostService

router = APIRouter(
    prefix='/blog'
)


@router.post('/create', response_model=PostReadOut, status_code=status.HTTP_201_CREATED)
async def create_post(request: PostCreateIn, service: PostService = Depends(PostService)):
    current_user_id = 1  # TODO: Will be replaced by current user
    return service.create(request, current_user_id)


@router.get('', response_model=list[PostReadOut], status_code=status.HTTP_200_OK)
async def list_posts(service: PostService = Depends(PostService)):
    return service.list()


@router.get('/{id}', response_model=PostReadOut, status_code=status.HTTP_200_OK)
async def get_post(id: int, service: PostService = Depends(PostService)):
    post = service.get(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post does not exist')
    return post
