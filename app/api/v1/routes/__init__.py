
from fastapi import APIRouter
from app.api.v1.routes import transcription,auth,audio


router = APIRouter()
router.include_router(transcription.router, prefix="/transcription", tags=["transcription"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(audio.router, prefix="/audio", tags=["audio"])