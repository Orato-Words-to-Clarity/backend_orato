import uuid
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.core.database import Base

class Audio(Base):
    __tablename__ = "audio"

    audio_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)  # Changed to UUID
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    language = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User")
    transcription = relationship("Transcription", back_populates="audio")