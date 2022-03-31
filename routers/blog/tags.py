from fastapi import APIRouter, Depends, status, HTTPException

from app.blog.schemas import Tag, TagReadOut
from app.blog.services import TagService

router = APIRouter(
    prefix='/tags'
)


@router.get('', response_model=list[Tag])
async def list_tags(service: TagService = Depends(TagService)):
    return service.list()


@router.get('/{id}', response_model=TagReadOut)
async def tag_posts(id: int, service: TagService = Depends(TagService)):
    return service.list_posts(id)
