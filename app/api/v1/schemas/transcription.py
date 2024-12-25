from pydantic import BaseModel

class Transcription(BaseModel):
    transcription: str