import json

from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Form, Body, Query

from app.accounts.models import User
from app.blog.schemas import PostRead, PostCreate, TagCreate, PostUpdate
from app.blog.services import PostService, CommentService, TagService
from app.blog.schemas import CommentCreate, CommentRead

import cloudinary
import cloudinary.uploader

from core.security import get_current_active_user

router = APIRouter(
    prefix='/blog'
)


@router.post('/create', response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create(title: str = Form(...),
                 body: str = Form(...),
                 file: UploadFile | None = None,
                 service: PostService = Depends(PostService),
                 tags: TagCreate = Body(None),
                 tag_service: TagService = Depends(TagService),
                 current_user: User = Depends(get_current_active_user)):

    request = {
        'title': title,
        'body': body
    }
    current_user_id = current_user.id
    url = None
    if file:
        result = cloudinary.uploader.upload(file.file)
        url = result.get("url", None)
    post = service.create(request, current_user_id, url)
    tag_service.create(tags, post)
    return post


@router.get('', response_model=list[PostRead], status_code=status.HTTP_200_OK)
async def get_all(query: str | None = None, service: PostService = Depends(PostService)):
    return service.list(query)


@router.get('/{id}', status_code=status.HTTP_200_OK)
async def get(id: int,
              service: PostService = Depends(PostService)):

    post = service.get(id)
    comments = service.list_comments(id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='post does not exist')
    return {
        "post": post,
        "comments": comments
    }


@router.patch('/{id}', status_code=status.HTTP_200_OK)
async def update(id: int,
                 request: PostUpdate,
                 service: PostService = Depends(PostService),
                 current_user: User = Depends(get_current_active_user)):

    current_user_id = current_user.id
    post = service.put(id, request, current_user_id)
    if post:
        return {'msg': 'Successfully updated post'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with id {id} does not exist')


@router.delete('/{id}', status_code=status.HTTP_202_ACCEPTED)
async def delete(id: int,
                 service: PostService = Depends(PostService),
                 current_user: User = Depends(get_current_active_user)):

    current_user_id = current_user.id
    post = service.get(id)
    if post:
        service.destroy(id, current_user_id)
        return {'msg': 'deleted successfully'}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f'Post with id {id} does not exist')


@router.post('/{post_id}/comment', response_model=CommentRead, status_code=status.HTTP_201_CREATED, tags=['comments'])
async def create_comment(post_id: int,
                         request: CommentCreate,
                         service: CommentService = Depends(CommentService),
                         current_user: User = Depends(get_current_active_user)):

    current_user_id = current_user.id
    return service.create(request, current_user_id, post_id)


@router.post('/{post_id}/{comment_id}/reply', status_code=status.HTTP_201_CREATED, tags=['comments'])
async def create_reply(post_id: int,
                       comment_id: int,
                       request: CommentCreate,
                       service: CommentService = Depends(CommentService),
                       current_user: User = Depends(get_current_active_user)):

    current_user_id = current_user.id
    return service.create(request, current_user_id, post_id, comment_id)
