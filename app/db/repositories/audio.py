from sqlalchemy.orm import Session
from app.db.models.audio import Audio
from app.db.models.transcription import Transcription

def get_all_audios(db: Session):
    return db.query(Audio).all()

def get_audio_with_transcription(db: Session, audio_id: int):
    return db.query(Audio).filter(Audio.audio_id == audio_id).first()