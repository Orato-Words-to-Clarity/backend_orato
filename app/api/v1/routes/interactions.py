from fastapi import APIRouter,Depends
from app.api.v1.schemas.interactions import CreateRequest
from app.api.v1.schemas.transcription import Transcription, TranscriptionRequest
from app.db.models.audio import Audio
from app.db.repositories.transcription import get_transcription_using_id
from app.services.interaction_service import get_create_generated_content
from app.utils.response_utils import ResponseHandler, ResponseModel
from app.utils.auth import get_current_user
from app.db.models.user import User
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.schemas.interactions import RequestType

router = APIRouter()

@router.post("/create/",response_model=ResponseModel)
def create_interaction(request: CreateRequest, db: Session= Depends(get_db), user: User= Depends(get_current_user)):
    
    prompt_mapping = {
        RequestType.MEETING_MINUTES: "Generate Detailed Meeting Minutes from the following transcription given below.",
        RequestType.CLASS_NOTES: " Summarize the following transcription into class notes.",
        RequestType.SUMMMARY: "Provide a concise summmary  of the follwing transcription.",
        RequestType.CUSTOM: request.custom_prompt,
    }
    
    transcription = get_transcription_using_id(db,request.transcription_id,user)
    
    # Send a prompt to Llama to get generated response
    structured_prompt = f"""
                You are an AI assistant tasked with generating structured and professional {request.request_type} format.
                {prompt_mapping[request.request_type]}  
                
                Below is the input content:

                [CONTENT]:  
                {transcription.text}  

                Follow these instructions:  
                1. Ensure clarity and conciseness.  
                2. Maintain a formal and professional tone.  
                3. Structure the response appropriately:
                - **For meeting minutes:** Include date, time, attendees, agenda, key discussions, decisions made, and action items.  
                - **For class notes:** Use bullet points or headings for different topics, summarize key concepts, and highlight important points.  
                - **For summaries:** Extract main ideas, key takeaways, and supporting details in a structured manner.  
                - **For custom format:** Adhere to the user-specified style and structure.  
                4. I want the generated content to be convertible into pdf, text or doc format. 

                Generate a well-formatted output based on these guidelines.
        """

            
            
    # Send the prompt to Llama and get the generated content
    generated_content = get_create_generated_content(structured_prompt)
    
    return ResponseHandler.success(message="Content Generated Successfully", data=generated_content)
    