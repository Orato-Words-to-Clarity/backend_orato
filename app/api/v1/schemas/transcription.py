from pydantic import BaseModel


class TranscriptionRequest(BaseModel):
    audio_id: str
    
class TranscriptionModel(BaseModel):
    transcription: str
    

class TranscriptionEditRequest(BaseModel):
    transcription_id: str
    text: str