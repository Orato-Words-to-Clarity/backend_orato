import os
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.v1.routes import users, router as api_router,auth

load_dotenv()
app = FastAPI()

app.include_router(users.router, prefix="/api/v1")
app.include_router(api_router, prefix="/api/v1")

@app.get('/')
def read_root():
    return {"message": "Hello World!! The backend server is running and live for API Testing !!"}