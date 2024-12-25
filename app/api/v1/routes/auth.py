import os
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.v1.schemas.user import UserCreate, UserResponse
from app.api.v1.schemas.token import Token, TokenData
from app.core.database import get_db
from app.db.repositories.user import create_user, get_user_by_username, get_user_by_email
from app.utils.auth import authenticate_user, create_access_token, create_refresh_token, get_current_user
from app.utils.response_utils import ResponseHandler, ResponseModel


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user_by_username = get_user_by_username(db, username=user.username)
    db_user_by_email = get_user_by_email(db, email=user.email)
    if db_user_by_username:
        raise HTTPException(status_code=400, detail="Username already registered")
    if db_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = create_user(db=db, user=user)
    return created_user

@router.post("/login", response_model=ResponseModel[Token])
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return ResponseHandler.error(
            "Incorrect username or password",
            status_code=400,
            details={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return ResponseHandler.success(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        },
        message="Login successful"
    )

@router.post("/refresh", response_model=ResponseModel[Token])
def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return ResponseHandler.error("Invalid refresh token", status_code=401)
    except JWTError:
        return ResponseHandler.error("Invalid refresh token", status_code=401)

    user = get_user_by_username(db, username=username)
    if user is None:
        return ResponseHandler.error("User not found", status_code=401)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return ResponseHandler.success(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        },
        message="Token refreshed successfully"
    )
