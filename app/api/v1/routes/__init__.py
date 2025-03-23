
from fastapi import APIRouter
from app.api.v1.routes import interactions, transcription,auth,audio,api,users


router = APIRouter()
router.include_router(transcription.router, prefix="/transcription", tags=["transcription"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(audio.router, prefix="/audio", tags=["audio"])
router.include_router(interactions.router, prefix="/interactions", tags=["interactions"]) 
router.include_router(api.router, prefix="/api", tags=["api"])
router.include_router(users.router, prefix="/user", tags=["user"])