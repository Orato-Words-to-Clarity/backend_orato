import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.v1.routes import users, router as api_router,auth
from fastapi.middleware.cors import CORSMiddleware
from app.utils.auth_middleware import create_auth_middleware

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Add authentication middleware
create_auth_middleware(app)

app.include_router(users.router, prefix="/api/v1")
app.include_router(api_router, prefix="/api/v1")

@app.get('/')
def read_root():
    return {"message": "Hello World!! The backend server is running and live for API Testing !!"}