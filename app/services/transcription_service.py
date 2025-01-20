from io import BytesIO
import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize the Groq client
api_key =  os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

def transcribe_audio(file_path: str) -> str:
    """
    Transcribe audio using the Groq Whisper API.
    :param file_path: Path to the audio file which is a url to the file stored in Azure Blob Storage.
    :return: Transcribed text or error message
    """
    try:
        # Get the audio file from Azure Blob Storage
        
        response = requests.get(file_path)
        response.raise_for_status()
        audio_content = BytesIO(response.content)
        audio_content.name = file_path.split('/')[-1]
        
        transcription = client.audio.transcriptions.create(
        
            file=audio_content , # Required audio file
            model="whisper-large-v3",  # Required model to use for transcription
            )
        
        return transcription.text
    except Exception as e:
        return f"An error occurred: {str(e)}"
