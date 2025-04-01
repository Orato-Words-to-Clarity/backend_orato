from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()

class UsageLimit(Base):
    __tablename__ = "usage_limits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey('users.id'), nullable=False, index=True)  # ForeignKey reference to users table
    date = Column(Date, nullable=False, default=date.today)
    total_llama_tokens = Column(Integer, nullable=False, default=0)
    total_whisper_tokens = Column(Integer, nullable=False, default=0)

    user = relationship("User", back_populates="usage_limits")  # Optional: to allow easy access to related user data
