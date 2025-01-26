from io import BytesIO
import os
import requests
from groq import Groq
from dotenv import load_dotenv
from langdetect import detect, LangDetectException


load_dotenv()

# Initialize the Groq client
api_key =  os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# Mapping from language codes to language names
LANGUAGE_CODES_TO_NAMES = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'bg': 'Bulgarian',
    'bn': 'Bengali',
    'da': 'Danish',
    'de': 'German',
    'el': 'Greek',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'hi': 'Hindi',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'ko': 'Korean',
    'lt': 'Lithuanian',
    'lv': 'Latvian',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'ne': 'Nepali',
    'pa': 'Punjabi',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese',
}

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
        



        # Extract the transcribed text
        transcribed_text = transcription.text
        
        # Detect the language of the transcribed text
        try:
            language_code = detect(transcribed_text)
            language = LANGUAGE_CODES_TO_NAMES.get(language_code, "unknown")
        except LangDetectException as e:
            language = "unknown"
            print(f"Language detection error: {str(e)}")

        return {
            "text": transcribed_text,
            "language": language
        }
        
    except Exception as e:
        return f"An error occurred: {str(e)}"
