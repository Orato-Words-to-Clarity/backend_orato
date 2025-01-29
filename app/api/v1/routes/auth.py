import os
from datetime import timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.api.v1.schemas.user import UserCreate, UserResponse
from app.api.v1.schemas.token import Token
from app.core.database import get_db
from app.db.repositories.user import create_user, get_user_by_username, get_user_by_email
from app.utils.auth import authenticate_user, create_access_token, create_refresh_token,validate_email
from app.utils.response_utils import ResponseHandler, ResponseModel

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 1440))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter()

@router.post("/register/", response_model=ResponseModel[UserResponse])
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    if(not validate_email(user.email)):
        return ResponseHandler.error("Invalid email address", status_code=400)
    
    db_user_by_email = get_user_by_email(db, email=user.email)
    if db_user_by_email:
        return ResponseHandler.error("Email already registered", status_code=400)
    created_user = create_user(db=db, user=user)
    user_response = UserResponse.model_validate(created_user)
    return ResponseHandler.success(data=user_response, message="User registered successfully")

@router.post("/login/", response_model=ResponseModel[Token])
def login_for_access_token(email: str = Form(...), password: str = Form(...),db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        return ResponseHandler.error(
            "Incorrect username or password",
            status_code=400,
            details={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )
    return ResponseHandler.success(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        },
        message="Login successful"
    )
    

class RefreshTokenRequestBody(BaseModel):
    refresh_token: str

@router.post("/refresh/", response_model=ResponseModel[Token])
def refresh_access_token(body: RefreshTokenRequestBody, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return ResponseHandler.error("Invalid refresh token", status_code=401)
    except JWTError:
        return ResponseHandler.error("Invalid refresh token", status_code=401)

    user = get_user_by_email(db, email=email)
    if user is None:
        return ResponseHandler.error("User not found", status_code=401)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return ResponseHandler.success(
        data={
            "access_token": access_token,
            "refresh_token": body.refresh_token,
            "token_type": "bearer"
        },
        message="Token refreshed successfully"
    )
