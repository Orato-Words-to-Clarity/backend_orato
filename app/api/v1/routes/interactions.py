from fastapi import APIRouter,Depends
from app.api.v1.schemas.interactions import AskRequest, CreateRequest
from app.api.v1.schemas.transcription import Transcription, TranscriptionRequest
from app.db.models.audio import Audio
from app.db.repositories.transcription import get_transcription_using_id
from app.services.interaction_service import get_create_generated_content, get_answer_to_query
from app.utils.response_utils import ResponseHandler, ResponseModel
from app.utils.auth import get_current_user
from app.db.models.user import User
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.v1.schemas.interactions import RequestType
from app.services.embedding_service import transcript_processor

router = APIRouter()

@router.post("/create/",response_model=ResponseModel[str])
def create_interaction(request: CreateRequest, db: Session= Depends(get_db), user: User= Depends(get_current_user)):
    
    prompt_mapping = {
        RequestType.MEETING_MINUTES: "Generate Detailed Meeting Minutes from the following transcription given below.",
        RequestType.CLASS_NOTES: " Summarize the following transcription into class notes.",
        RequestType.SUMMMARY: "Provide a concise summmary  of the follwing transcription.",
        RequestType.CUSTOM: request.custom_prompt,
    }
    
    transcription = get_transcription_using_id(db,request.transcription_id,user)
    
    # Send a prompt to Llama to get generated response
    structured_prompt =  f"""
                Generate a structured and professional {request.request_type} in **HTML format only**.

                [PROMPT]:  
                {prompt_mapping[request.request_type]}  

                [TRANSCRIPTION]:  
                {transcription.text}  

                [STRICT OUTPUT FORMAT]:  
                - The response **must be valid HTML** with no additional text, comments, or explanations.  
                - **DO NOT** include any non-HTML content or extra remarks.  
                - **DO NOT** mix formats—strictly follow the correct structure as defined below.
                - **MUST** use tailwind styles for styling purposes  

                [STRICT RULES]:  
                - **Meeting Minutes (ONLY if requested):**  
                  - **MUST contain:** Date, time, attendees, agenda, key discussions, decisions made, and action items.  
                  - **Use headings and lists** for structured representation.  
                  - **DO NOT use paragraphs; use structured HTML elements.**  

                - **Class Notes (ONLY if requested):**  
                  - **MUST contain:** Headings, bullet points, and structured sections.  
                  - **DO NOT use paragraph-based summaries; ensure clarity with structured elements.**  

                - **Summaries (ONLY if requested):**  
                  - **MUST contain:** Extracted main ideas and key takeaways.  
                  - **MUST be in paragraph format ONLY—NO bullet points or lists.**  
                  - **DO NOT include agenda, attendees, or action items (these belong to meeting minutes).**  

                - **Custom Format (STRICTLY FOLLOW USER INPUT):**  
                  - **DO NOT assume any structure. Follow the exact instructions provided by the user.**  
                  - **DO NOT default to meeting minutes.**  
                  - **If the user does not specify a format, return only the transcription as HTML text.**  
                  - **Ignore all other formats unless explicitly stated.**  

                [IMPORTANT]:  
                - **FOLLOW THE RULES STRICTLY. DO NOT DEVIATE.**  
                - **NO INTRODUCTIONS, NO CONCLUSIONS, NO EXTRA TEXT—ONLY RETURN THE HTML.**  
                - **DO NOT return markdown, plain text, or any explanations—only well-formatted HTML.**
                - **MUST ONLY use tailwind for styling**   
"""

            
            
    # Send the prompt to Llama and get the generated content
    generated_content = get_create_generated_content(structured_prompt)
    
    return ResponseHandler.success(message="Content Generated Successfully", data=generated_content)
    
    



@router.post("/ask",response_model=ResponseModel[str])
def ask_question(request: AskRequest, db: Session= Depends(get_db), user: User= Depends(get_current_user)):
    
    results = transcript_processor.query_similar_sentences(request.query, request.transcription_id, top_k=3)
  
    prompt = f"""
            You are an expert assistant answering queries based on provided relevant information.

            [CONTEXT]:  
            Below are sentences retrieved from a knowledge base along with their relevance scores. 
            Higher scores indicate stronger relevance to the question.

            {results}

            [QUESTION]:  
            {request.query}

            [RULES]:  
            1. Use the most relevant sentences (higher scores) first to form your answer.
            2. Summarize the key information clearly and concisely.
            3. Avoid making up details not present in the context.
            4. If the context lacks enough information to answer the question, respond with:  
              "I don't have enough information to answer this."

            Provide your answer below:
        """
    # Send the prompt to Llama and get the generated content
    generated_content = get_answer_to_query(prompt)
    
    return ResponseHandler.success(message="Content Generated Successfully", data=generated_content)
  
  
  