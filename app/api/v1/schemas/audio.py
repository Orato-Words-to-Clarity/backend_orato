from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional



class TranscriptionResponse(BaseModel):
    transcription_id: int
    audio_id: int
    text: str
    embedding_id: Optional[int]
    language: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class AudioResponse(BaseModel):
    audio_id: int
    file_path: str
    file_name: str
    language: str
    created_at: datetime

    class Config:
        from_attributes = True

class AudioWithTranscriptionResponse(AudioResponse):
    transcription: TranscriptionResponse

class UploadAudioResponse(BaseModel):
    audio_id: str
    file_path: str
    file_name: str
    
    