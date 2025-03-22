import enum
from typing import Literal
from pydantic import BaseModel


class RequestType(str, enum.Enum):
    MEETING_MINUTES = "meeting_minutes"
    CLASS_NOTES = "class_notes"
    SUMMMARY = "summary"
    CUSTOM = "custom"

class CreateRequest(BaseModel):
    request_type: Literal["meeting_minutes", "class_notes", "summary", "custom"]
    custom_prompt: str = ""
    transcription_id: str
    
    
class AskRequest(BaseModel):
    query: str
    transcription_id: str