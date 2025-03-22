from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class APIKey(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)  # Linked to User
    groq_api_key_encrypted = Column(String, nullable=True)
    huggingface_api_key_encrypted = Column(String, nullable=True)

    user = relationship("User", back_populates="api_keys")  # No need to import User
