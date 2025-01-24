from sqlalchemy.orm import Session, joinedload
from app.db.models.audio import Audio
from app.db.models.user import User

def get_all_audios(db: Session,user: User): 
    return db.query(Audio).filter(Audio.user_id == user.id).all()

def get_audio_details(db: Session, audio_id: int):
    return db.query(Audio).options(joinedload(Audio.transcription)).filter(Audio.audio_id == audio_id).first()

def create_audio(db: Session, current_user:User, blob_url:str, file_name:str):
    audio = Audio(user_id=current_user.id, file_path=blob_url, file_name=file_name)
    db.add(audio)
    db.commit()
    db.refresh(audio)
    return audio