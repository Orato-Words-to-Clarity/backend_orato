# FastAPI Project

A scalable FastAPI application with PostgreSQL integration, following the repository pattern for clean architecture. This project includes JWT-based authentication, secure password hashing, and manual database migrations.

## Features
- FastAPI framework for building APIs
- PostgreSQL as the database
- JWT authentication and password hashing
- Organized repository pattern for database operations
- Manual migrations for database schema changes

## Quick Start
1. Clone the repository and navigate to the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Set up your environment variables in `.env` (refer to `.env.sample` for structure).
4. Run the app with the following command:
   ```bash
   python run.py

The app will be live at `http://127.0.0.1:8000` with interactive API docs at `/docs`.
