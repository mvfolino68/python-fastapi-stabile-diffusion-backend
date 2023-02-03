from fastapi import APIRouter

from image.routers.v1.generate import router as image_api

router = APIRouter()

router.include_router(image_api, prefix="/image", tags=["image"])
