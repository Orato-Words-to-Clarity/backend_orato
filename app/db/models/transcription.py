from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Transcription(Base):
    __tablename__ = "transcriptions"

    transcription_id = Column(Integer, primary_key=True, index=True)
    audio_id = Column(Integer, ForeignKey("audio.audio_id"), nullable=False)
    text = Column(String, nullable=False)
    embedding_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    audio = relationship("Audio", back_populates="transcriptions")