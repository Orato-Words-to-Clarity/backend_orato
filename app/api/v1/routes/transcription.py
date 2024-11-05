import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.transcription_service import transcribe_audio
import tempfile

router = APIRouter()

@router.post("/transcribe/")
async def transcribe(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    # Perform transcription
    transcription_result = transcribe_audio(temp_file_path)

    # Clean up the temporary file
    os.remove(temp_file_path)

    # Return the transcription result
    if "An error occurred" in transcription_result:
        raise HTTPException(status_code=500, detail=transcription_result)

    return {"transcription": transcription_result}
