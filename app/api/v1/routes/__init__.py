
from fastapi import APIRouter
from app.api.v1.routes import transcription

router = APIRouter()
router.include_router(transcription.router, prefix="/transcription", tags=["transcription"])
