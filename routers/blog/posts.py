from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Form

from app.blog.schemas import PostReadOut, PostCreateIn, CommentCreateIn
from app.blog.services import PostService, CommentService

import cloudinary
import cloudinary.uploader

router = APIRouter(
    prefix='/blog'
)


@router.post('/create', response_model=PostReadOut, status_code=status.HTTP_201_CREATED)
async def create_post(title=Form(...), body=Form(...), file: UploadFile | None = None,
                      service: PostService = Depends(PostService)):
    request = {
        'title': title,
        'body': body
    }
    current_user_id = 1  # TODO: Will be replaced by current user
    url = None
    if file:
        result = cloudinary.uploader.upload(file.file)
        url = result.get("url", None)
    return service.create(request, current_user_id, url)


@router.get('', response_model=list[PostReadOut], status_code=status.HTTP_200_OK)
async def list_posts(service: PostService = Depends(PostService)):
    return service.list()


@router.get('/{id}', response_model=PostReadOut, status_code=status.HTTP_200_OK)
async def get_post(id: int, service: PostService = Depends(PostService)):
    post = service.get(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post does not exist')
    return post


@router.put('/{id}', status_code=status.HTTP_200_OK)
async def update(id: int, request: PostCreateIn, service: PostService = Depends(PostService)):
    current_user_id = 1
    post = service.put(id, request, current_user_id)
    if post:
        return {'msg': 'Successfully updated post'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} does not exist')


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def delete(id: int, service: PostService = Depends(PostService)):
    current_user_id = 1
    post = service.get(id)
    if post:
        service.destroy(id, current_user_id)
        return {'msg': 'deleted successfully'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id {id} does not exist')
