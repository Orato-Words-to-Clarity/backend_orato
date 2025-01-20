import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
from app.core.database import Base

class Transcription(Base):
    __tablename__ = "transcriptions"

    transcription_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  # Changed to UUID
    audio_id = Column(UUID(as_uuid=True), ForeignKey("audio.audio_id"), nullable=False)  
    text = Column(String, nullable=False)
    embedding_id = Column(Integer, nullable=True)
    language = Column(String, nullable=True)  # Add the language field
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    audio = relationship("Audio", back_populates="transcription")