from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class UserApiKeyResponse(BaseModel):
    email: str
    groq_api_key: str | None
    huggingface_api_key: str | None

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True