from fastapi import APIRouter, Depends
from app.core.database import get_db
from app.db.models.user import User
from app.utils.auth import get_current_user
from sqlalchemy.orm import Session
router = APIRouter()

@router.get("/users/", tags=["users"])
async def read_users(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return [{"username": "user1"}, {"username": "user2"}]
