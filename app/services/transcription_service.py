import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
api_key =  os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio using the Groq Whisper API.
    :param file_path: Path to the audio file
    :return: Transcribed text or error message
    """
    try:
        with open(file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(os.path.basename(file_path), file.read()),  # Required audio file
                model="whisper-large-v3",  # Required model to use for transcription
            )
            return transcription.text
    except Exception as e:
        return f"An error occurred: {str(e)}"
