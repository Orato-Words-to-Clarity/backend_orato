from io import BytesIO
import os
import requests
from groq import Groq
from dotenv import load_dotenv


load_dotenv()

# Initialize the Groq client
api_key =  os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


def get_create_generated_content(prompt: str):


    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Use "llama3-8b" if you need LLaMA 3
        messages=[
            {"role": "system", "content": "You are a Professional Html Designer and Content Creator/Writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    
    return response.choices[0].message.content
    