import os
import subprocess

def run_migrations():
    """
    Run the migration script before starting the server.
    """
    print("Running database migrations...")
    try:
        # Run the migrate.py script
        subprocess.run(["python", "migrate.py"], check=True)
        print("Migrations applied successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error applying migrations: {e}")
        exit(1)
    

if __name__ == "__main__":
    import uvicorn

    # Step 1: Run migrations
    run_migrations()

    # Step 2: Start the FastAPI app
    port = int(os.getenv("PORT", 8000))  # Default to 8000 if PORT is not set
    host = os.getenv("HOST", "0.0.0.0")  # Default to 127.0.0.1 if HOST is not set
    uvicorn.run("app.main:app", host=host, port=port, reload=True)
