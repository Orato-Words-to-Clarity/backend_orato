import os

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    host = os.getenv("HOST", "127.0.0.1")  # Default to 127.0.0.1 if HOST is not set
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
