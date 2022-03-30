from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, Form

from app.blog.schemas import TagReadOut
from app.blog.services import TagService

router = APIRouter(
    prefix='/tags'
)


@router.post('', response_model=list[TagReadOut])
async def list_tags(service: TagService = Depends(TagService)):
    return service.list()
