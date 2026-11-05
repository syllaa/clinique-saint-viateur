from fastapi import APIRouter, Depends, File, UploadFile

from app.auth.dependencies import require_admin
from app.uploads import service

router = APIRouter(prefix="/api/uploads", tags=["uploads"], dependencies=[Depends(require_admin)])


@router.post("/images")
async def upload_image(file: UploadFile = File(...)):
    filename = await service.save_image(file)
    return {"url": service.image_url(filename)}
