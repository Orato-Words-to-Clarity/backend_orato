from fastapi import FastAPI
from app.api.v1.routes import users, router as api_router

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")
app.include_router(api_router, prefix="/api/v1")