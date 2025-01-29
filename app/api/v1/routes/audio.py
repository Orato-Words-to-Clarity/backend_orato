import os
import uuid
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.user import User
from app.db.repositories.audio import create_audio, get_all_audios, get_audio_details
from app.api.v1.schemas.audio import AudioResponse, AudioWithTranscriptionResponse, UploadAudioResponse

from typing import List

from app.utils.auth import get_current_user
from app.utils.response_utils import ResponseHandler, ResponseModel
from azure.storage.blob import BlobServiceClient, ContentSettings

router = APIRouter()


ALLOWED_AUDIO_TYPES = ["audio/mpeg", "audio/wav", "audio/ogg", "audio/flac", "audio/mp3"]

@router.get("/", response_model=ResponseModel[List[AudioResponse]])
def get_audios(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Retrieve all audios for the authenticated user
    audios = get_all_audios(db, current_user)
    if not audios:
        return ResponseHandler.success([],"No audios found for the user", status_code=200)
    audio_data = [AudioResponse.model_validate(audio) for audio in audios]
    return ResponseHandler.success(audio_data, message="Audios retrieved successfully")



@router.get("/{audio_id}/", response_model=ResponseModel[AudioWithTranscriptionResponse])
def get_audio_with_transcription(audio_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    audio = get_audio_details(db, audio_id)
    if not audio:
        return ResponseHandler.error("Audio not found", status_code=404)
    if(audio.user_id != current_user.id):
        return ResponseHandler.error("You don't have permission to access this audio", status_code=403)
    print(audio.transcription)
    return ResponseHandler.success(AudioWithTranscriptionResponse.model_validate(audio), message="Audio retrieved successfully")



@router.post("/upload-audio/", response_model=ResponseModel[UploadAudioResponse])
async def upload_audio(file: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # TODO: Implement audio upload logic
    # Check the content type to make sure it's an audio file
    if file.content_type not in ALLOWED_AUDIO_TYPES:
        ResponseHandler.error("Invalid file type. Please upload a valid audio file.", status_code=400)

    # Optional: Check the file extension if you want extra validation
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in [".mp3", ".wav", ".ogg", ".flac"]:
        ResponseHandler.error("Invalid file extension. Allowed extensions are .mp3, .wav, .ogg, .flac.", status_code=400)
    
    
    try:

        # Get the Azure Blob Storage credentials from the environment variables
        AZURE_STORAGE_CONTAINER_NAME = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        
        # Initialize the BlobServiceClient
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        file_extension = os.path.splitext(file.filename)[1]  # Extract the file extension
        unique_filename = f"{uuid.uuid4()}{file_extension}"

        # Blob name with folder path (optional)
        blob_name = f"{unique_filename}"

        # Get the container client
        container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)

        # Upload the file to Azure Blob Storage
        blob_client = container_client.get_blob_client(blob_name)

        # Read file content and upload
        blob_client.upload_blob(
            await file.read(),
            overwrite=True,
            content_settings=ContentSettings(content_type=file.content_type),
        )

        # Construct the blob URL
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_STORAGE_CONTAINER_NAME}/{blob_name}"

        # Save the audio record in the database
        audio = create_audio(db, current_user, blob_url, file.filename)
        

        return ResponseHandler.success(
            message="Audio uploaded successfully", 
            data={    
                "audio_id": str(audio.audio_id), 
                "file_path": audio.file_path, 
                "file_name": audio.file_name 
                }
            )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))