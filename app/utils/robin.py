import os
import itertools
from app.utils.enums import Provider
from dotenv import load_dotenv

load_dotenv()

groq_api_keys = os.getenv("GROQ_API_KEY").split(",")
huggingface_api_keys = os.getenv("HUGGING_FACE_API_KEY").split(",")

groq_cycle = itertools.cycle(groq_api_keys)
huggingface_cycle = itertools.cycle(huggingface_api_keys)


def get_next_api_key(provider: Provider) -> str:
    """
    Retrieves and decrypts the API key for the current authenticated user.

    :param provider: The API provider name ('groq' or 'huggingface').
    :return: The decrypted API key or a default API key.
    """
    if provider == Provider.GROQ:
        return next(groq_cycle)
    elif provider == Provider.HUGGINGFACE:
        return next(huggingface_cycle)
    else:
        return None  # Return None if provider is invalid
    