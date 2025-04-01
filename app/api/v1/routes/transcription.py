import uuid
from sqlalchemy.orm import joinedload
from fastapi import APIRouter,Depends
from app.api.v1.schemas.transcription import TranscriptionModel, TranscriptionEditRequest, TranscriptionRequest
from app.db.models.audio import Audio
from app.db.models.transcription import Transcription
from app.db.repositories.transcription import update_transcription
from app.services.transcription_service import transcribe_audio
from app.utils.response_utils import ResponseHandler, ResponseModel
from app.utils.auth import get_current_user
from app.db.models.user import User
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.embedding_service import TranscriptProcessor
from app.utils.usage import check_usage_limit, estimate_tokens, update_usage


router = APIRouter()




@router.post("/transcribe/", response_model=ResponseModel[TranscriptionModel])
async def transcribe(request: TranscriptionRequest,  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
     
    if check_usage_limit(user.id, "whisper", db):
        return ResponseHandler.error(
            message="Usage limit exceeded",
            status_code=429,
            details={"usage_limit": "You have exceeded your usage limit for transcription today."}
        )
    
    # Get the audio file url from the db using audio id
    audio: Audio | None = db.query(Audio).filter(Audio.audio_id == request.audio_id).first()
    if not audio:
        ResponseHandler.error(message="Audio not found", status_code=400)
    
    transcription_result = transcribe_audio(audio.file_path,db,user)

    # Return the transcription result
    if "An error occurred" in transcription_result:
        return ResponseHandler.error(
            message="Failed to transcribe the audio",
            details=transcription_result,
            status_code=500
        )
        
    output_tokens = estimate_tokens(transcription_result["text"])
    update_usage(user.id, "whisper", output_tokens , db)
        
    transcription_result["transcription_id"] = update_transcription(db,audio.audio_id, transcription_result["text"], transcription_result["language"])

    transcript_processor=TranscriptProcessor(db,user)

    transcript_processor.accept_transcript(transcription_result["text"])
    transcript_processor.split_into_sentences()
    transcript_processor.generate_embeddings()
    transcript_processor.upsert_embeddings_to_pinecone(transcription_result["transcription_id"])
    

    return ResponseHandler.success(
        data={"transcription": transcription_result},
        message="Transcription successful"
    )


@router.patch('/edit/', response_model=ResponseModel[TranscriptionModel])
async def edit_transcription(request: TranscriptionEditRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Get the transcription from the db using transcription id
    print(request.transcription_id)

    transcription = db.query(Transcription).options(joinedload(Transcription.audio)).filter(Transcription.transcription_id == request.transcription_id).first()


    if not transcription:
        ResponseHandler.error(message="Transcription not found", status_code=400)
    
    if(transcription.audio.user_id != user.id):
        ResponseHandler.error(message="You don't have permission to access this transcription", status_code=403)

    transcription.text = request.text
    db.commit()

    return ResponseHandler.success(
        data={"transcription": request.text},
        message="Transcription edited successfully"
    )