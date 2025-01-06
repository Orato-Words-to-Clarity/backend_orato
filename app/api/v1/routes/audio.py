from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.repositories.audio import get_all_audios, get_audio_with_transcription
from app.api.v1.schemas.audio import AudioResponse, AudioWithTranscriptionResponse

from typing import List

router = APIRouter()

@router.get("/audios", response_model=List[AudioResponse])
def get_audios(db: Session = Depends(get_db)):
    audios = get_all_audios(db)
    return audios


@router.get("/audios/{audio_id}", response_model=AudioWithTranscriptionResponse)
def get_audio_with_transcription(audio_id: int, db: Session = Depends(get_db)):
    audio = get_audio_with_transcription(db, audio_id)
    if not audio:
        raise HTTPException(status_code=404, detail="Audio not found")
    return audio