from fastapi import APIRouter

from image.routers.v1.generate import router as image_generate_router
from image.routers.v1.image import router as image_api

router = APIRouter()

router.include_router(image_generate_router, prefix="/image-generator", tags=["image-generator"])
router.include_router(image_api, prefix="/image-db", tags=["image-db"])
