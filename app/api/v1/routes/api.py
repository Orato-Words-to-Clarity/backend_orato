# route to receive api key from the user 

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.db.models.api_keys import APIKey
from app.api.v1.schemas.api_keys import APIKeyBase, APIKeyCheckResponse, APIKeyCreate,APIKeyResponse
from app.utils.auth import get_current_user
from app.utils.response_utils import ResponseHandler, ResponseModel
from cryptography.fernet import Fernet
import os

from app.db.models.user import User

router = APIRouter()
cipher = Fernet(os.getenv("ENCRYPTION_KEY"))



@router.post("/set-api-key/", response_model=ResponseModel[APIKeyResponse])
def set_api_key(request: APIKeyCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # set the user with the api key even it already exits or if it is null
    if not request:
        ResponseHandler.error(message="Please provide the API Key")
    api_keys = db.query(APIKey).filter(APIKey.user_id == user.id).first() or APIKey(user_id=user.id)
    api_keys.groq_api_key_encrypted = cipher.encrypt(request.groq_api_key.encode()).decode() if request.groq_api_key else None
    api_keys.huggingface_api_key_encrypted = cipher.encrypt(request.huggingface_api_key.encode()).decode() if request.huggingface_api_key else None
    db.add(api_keys)
    db.commit()
    db.refresh(api_keys)
    return ResponseHandler.success(data=APIKeyResponse.model_validate(api_keys), message="API Key set successfully")


@router.get("/is-api-set/", response_model=ResponseModel[APIKeyCheckResponse])
def is_api_key_set(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    api_keys = db.query(APIKey).filter(APIKey.user_id == user.id).first()
    if not api_keys or not (api_keys.groq_api_key_encrypted and api_keys.huggingface_api_key_encrypted):
        return ResponseHandler.success(data={is_api_key_set:False}, message="API Key not set")
    
    return ResponseHandler.success(data={is_api_key_set:True}, message="API Key already set")