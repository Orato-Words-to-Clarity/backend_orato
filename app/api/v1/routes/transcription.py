import os
from typing import Any
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.api.v1.schemas.transcription import Transcription
from app.services.transcription_service import transcribe_audio
import tempfile
from app.utils.response_utils import ResponseHandler, ResponseModel

router = APIRouter()

from typing import Dict


@router.post("/transcribe", response_model=ResponseModel[Transcription])
async def transcribe(file: UploadFile = File(...)):
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
