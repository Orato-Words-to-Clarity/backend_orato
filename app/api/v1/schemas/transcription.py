from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    audio_id: str
    
class Transcription(BaseModel):
    transcription: str