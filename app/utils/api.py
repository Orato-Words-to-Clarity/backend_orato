from enum import Enum
import os
from typing import Literal
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from cryptography.fernet import Fernet
from fastapi import Depends
from app.db.models.api_keys import APIKey
from app.db.models.user import User  # Assuming you have a User model
from app.core.database import get_db  # Import dependency functions
from app.utils.auth import get_current_user
from app.utils.enums import Provider
from app.utils.robin import get_next_api_key  # Import dependency functions


load_dotenv()


# Load encryption key from environment
FERNET_SECRET_KEY = os.getenv("ENCRYPTION_KEY")
cipher_suite = Fernet(FERNET_SECRET_KEY)

def decrypt_api_key(encrypted_key: str) -> str:
    """Decrypts an encrypted API key using Fernet."""
    try:
        return cipher_suite.decrypt(encrypted_key.encode()).decode()
    except Exception as e:
        print(f"Error decrypting API key: {e}")
        return None  # Return None if decryption fails

def get_api_key(provider: Provider, db: Session, current_user: User) -> str:
    """
    Retrieves and decrypts the API key for the current authenticated user.
    If not found, it returns a default API key using a round-robin strategy.

    :param provider: The API provider name ('groq' or 'huggingface').
    :param db: The SQLAlchemy database session (injected via FastAPI dependency).
    :param current_user: The currently authenticated user (retrieved via FastAPI dependency).
    :return: The decrypted API key or a default API key.
    """
    api_key_entry = db.query(APIKey).filter(APIKey.user_id == current_user.id).first()

    if api_key_entry:
        if provider == Provider.GROQ and api_key_entry.groq_api_key_encrypted:
            decrypted_key = decrypt_api_key(api_key_entry.groq_api_key_encrypted)
            if decrypted_key:
                return decrypted_key  # Return decrypted key if successful

        elif provider == Provider.HUGGINGFACE and api_key_entry.huggingface_api_key_encrypted:
            decrypted_key = decrypt_api_key(api_key_entry.huggingface_api_key_encrypted)
            if decrypted_key:
                return decrypted_key  # Return decrypted key if successful

    # Default API keys found by using round robin strategy
    if provider == Provider.GROQ:
        return get_next_api_key(Provider.GROQ)
    elif provider == Provider.HUGGINGFACE:
        return get_next_api_key(Provider.HUGGINGFACE)
      # Return None if provider is invalid
    else:
        return None
