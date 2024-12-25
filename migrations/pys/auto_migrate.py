from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.db.models.user import User  # Import your models here

# Load environment variables from .env file
from dotenv import load_dotenv
import os

load_dotenv()

# Get the database URL from environment variables
DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_existing_tables(engine):
    inspector = inspect(engine)
    return inspector.get_table_names()

def create_tables():
    existing_tables = get_existing_tables(engine)
    if not existing_tables:
        Base.metadata.create_all(bind=engine)
        print("Tables created successfully.")
    else:
        print("Tables already exist. No changes made.")

if __name__ == "__main__":
    create_tables()