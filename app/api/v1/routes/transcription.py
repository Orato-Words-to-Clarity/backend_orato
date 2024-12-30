import os
from typing import Any
from fastapi import APIRouter, UploadFile, File, HTTPException,Depends
from app.api.v1.schemas.transcription import Transcription
from app.services.transcription_service import transcribe_audio
import tempfile
from app.utils.response_utils import ResponseHandler, ResponseModel
from app.utils.auth_middleware import get_current_user
from app.db.models.user import User
from sqlalchemy.orm import Session
from app.core.database import get_db



router = APIRouter()

from typing import Dict


@router.post("/transcribe", response_model=ResponseModel[Transcription])
async def transcribe(file: UploadFile = File(...),user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # Perform transcription
        transcription_result = transcribe_audio(temp_file_path)
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)

    # Return the transcription result
    if "An error occurred" in transcription_result:
        return ResponseHandler.error(
            message="Failed to transcribe the audio",
            details=transcription_result,
            status_code=500
        )

    return ResponseHandler.success(
        data={"transcription": transcription_result},
        message="Transcription successful"
    )
