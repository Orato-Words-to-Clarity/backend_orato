from uuid import UUID
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List, Optional



class TranscriptionResponse(BaseModel):
    transcription_id: str
    audio_id: str
    text: str
    embedding_id: Optional[int]
    language: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
        
    @field_validator("created_at", mode="before")
    def convert_datetime_to_str(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value
    
    @field_validator("transcription_id", mode="before")
    def convert_uuid_to_str(cls, value):
        if isinstance(value, UUID):
            return str(value)
        return value
    
    @field_validator("audio_id", mode="before")
    def convert_uuid_to_str(cls, value):
        if isinstance(value, UUID):
            return str(value)
        return value



class AudioResponse(BaseModel):
    audio_id: str
    file_path: str
    file_name: str
    language: str | None
    created_at: str

    class Config:
        from_attributes = True
    # Validator to convert UUID to string
    @field_validator("audio_id", mode="before")
    def convert_uuid_to_str(cls, value):
        if isinstance(value, UUID):
            return str(value)
        return value
    
    @field_validator("created_at", mode="before")
    def convert_datetime_to_str(cls, value):
        if isinstance(value, datetime):
            return value.strftime("%Y-%m-%d %H:%M:%S")
        return value

class AudioWithTranscriptionResponse(AudioResponse):
    transcription: TranscriptionResponse

class UploadAudioResponse(BaseModel):
    audio_id: str
    file_path: str
    file_name: str
    
    