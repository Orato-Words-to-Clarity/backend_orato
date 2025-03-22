from pydantic import BaseModel
from typing import Optional

class APIKeyBase(BaseModel):
    groq_api_key_encrypted: Optional[str] = None
    huggingface_api_key_encrypted: Optional[str] = None

class APIKeyCreate(APIKeyBase):
    groq_api_key: Optional[str] = None
    huggingface_api_key: Optional[str] = None

class APIKeyResponse(APIKeyBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True  # This allows conversion from SQLAlchemy models

class APIKeyCheckResponse(BaseModel):
    is_api_key_set: bool
    class Config:
        from_attributes = True  # This allows conversion from SQLAlchemy models