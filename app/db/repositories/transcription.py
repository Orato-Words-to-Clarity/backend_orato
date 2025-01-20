from sqlalchemy import  Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from app.db.models.audio import Audio
from app.db.models.transcription import Transcription
from app.utils.response_utils import ResponseHandler


def update_transcription(db: Session, audio_id:Column[UUID] , transcription:str):
    audio = db.query(Audio).filter(Audio.audio_id == audio_id).first()
    if not audio:
        return ResponseHandler.error("Audio not found",status_code=400)
    
    transcription_obj = db.query(Transcription).filter(Transcription.audio_id == audio_id).first()
    if  transcription_obj:
        transcription_obj.text = transcription
        db.commit()
    else:
        transcription_obj = Transcription(audio_id=audio_id,text=transcription)
        db.add(transcription_obj)
        db.commit()
    
   