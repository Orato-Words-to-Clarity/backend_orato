from fastapi import APIRouter, Depends
from app.api.v1.schemas.user import UserApiKeyResponse
from app.core.database import get_db
from app.db.models.api_keys import APIKey
from app.db.models.user import User
from app.utils.auth import get_current_user
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
import os

from app.utils.response_utils import ResponseHandler
router = APIRouter()
cipher = Fernet(os.getenv("ENCRYPTION_KEY"))

@router.get("/users/", tags=["users"])
async def read_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return [{"username": "user1"}, {"username": "user2"}]

@router.get("/")
async def read_root(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    api_keys = db.query(APIKey).filter(APIKey.user_id == current_user.id).first()
    if not api_keys:
        return ResponseHandler.success(data=UserApiKeyResponse.model_validate({
            "email": current_user.email,
            "groq_api_key": None,
            "huggingface_api_key": None
        }))



    return ResponseHandler.success(data=UserApiKeyResponse.model_validate({
        "email": current_user.email,
        "groq_api_key": cipher.decrypt(api_keys.groq_api_key_encrypted.encode()).decode() if api_keys.groq_api_key_encrypted else None,
        "huggingface_api_key": cipher.decrypt(api_keys.huggingface_api_key_encrypted.encode()).decode() if api_keys.huggingface_api_key_encrypted else None
    }))
    