from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date
from app.core.database import Base

class UsageLimit(Base):
    __tablename__ = "usage_limits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)  # ForeignKey reference to users table
    date = Column(Date, nullable=False, default=date.today)
    total_llama_tokens = Column(Integer, nullable=False, default=0)
    total_whisper_tokens = Column(Integer, nullable=False, default=0)

    # Use string 'User' to delay the lookup of the User class
    user = relationship("User", back_populates="usage_limits")

    def __repr__(self):
        return f"<UsageLimit(user_id={self.user_id}, date={self.date}, llama={self.total_llama_tokens}, whisper={self.total_whisper_tokens})>"
