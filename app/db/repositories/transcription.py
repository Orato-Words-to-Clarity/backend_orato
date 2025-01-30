from sqlalchemy import  Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session, joinedload
from app.db.models.audio import Audio
from app.db.models.transcription import Transcription
from app.db.models.user import User
from app.utils.response_utils import ResponseHandler


def update_transcription(db: Session, audio_id:Column[UUID] , transcription:str,language:str):
        
    audio = db.query(Audio).filter(Audio.audio_id == audio_id).first()
    if not audio:
        return ResponseHandler.error("Audio not found",status_code=400)
    
    transcription_obj = db.query(Transcription).filter(Transcription.audio_id == audio_id).first()
    if  transcription_obj:
        transcription_obj.text = transcription
        audio_obj = db.query(Audio).filter(Audio.audio_id == audio_id).first()
        audio_obj.language = language
        db.commit()
    else:
        transcription_obj = Transcription(audio_id=audio_id,text=transcription)
        audio_obj = db.query(Audio).filter(Audio.audio_id == audio_id).first()
        audio_obj.language = language
        db.add(transcription_obj)
        db.commit()
        
    return str(transcription_obj.transcription_id)
    
   
def get_transcription_using_id(db: Session, transcription_id: str, user: User):
    transcription = db.query(Transcription).options(joinedload(Transcription.audio)).filter(Transcription.transcription_id == transcription_id).first()

    if not transcription:
        return ResponseHandler.error("Transcription not found", status_code=400)
    
    if transcription.audio.user_id != user.id :
        return ResponseHandler.error("You don't have permission to access this transcription", status_code=403)
    
    return transcription