from fastapi import APIRouter,Depends
from app.api.v1.schemas.transcription import Transcription, TranscriptionRequest
from app.db.models.audio import Audio
from app.db.repositories.transcription import update_transcription
from app.services.transcription_service import transcribe_audio
from app.utils.response_utils import ResponseHandler, ResponseModel
from app.utils.auth import get_current_user
from app.db.models.user import User
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.embedding_service import transcript_processor


router = APIRouter()




@router.post("/transcribe/", response_model=ResponseModel[Transcription])
async def transcribe(request: TranscriptionRequest,  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Get the audio file url from the db using audio id
    audio: Audio | None = db.query(Audio).filter(Audio.audio_id == request.audio_id).first()
    if not audio:
        ResponseHandler.error(message="Audio not found", status_code=400)
    
    transcription_result = transcribe_audio(audio.file_path)

    # Return the transcription result
    if "An error occurred" in transcription_result:
        return ResponseHandler.error(
            message="Failed to transcribe the audio",
            details=transcription_result,
            status_code=500
        )
        
    transcription_result["transcription_id"] = update_transcription(db,audio.audio_id, transcription_result["text"], transcription_result["language"])

    transcript_processor.accept_transcript(transcription_result.text)
    transcript_processor.split_into_sentences()
    transcript_processor.generate_embeddings()
    transcript_processor.upsert_embeddings_to_pinecone(transcription_result["transcription_id"])
    

    return ResponseHandler.success(
        data={"transcription": transcription_result},
        message="Transcription successful"
    )