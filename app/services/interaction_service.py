from io import BytesIO
import os
import requests
from groq import Groq
from dotenv import load_dotenv
from app.utils.enums import Provider
from app.utils.api import get_api_key
from app.db.models.user import User
from sqlalchemy.orm import Session


load_dotenv()




def get_create_generated_content(prompt: str,db : Session,user : User) -> str:

    # Initialize the Groq client
    api_key =  get_api_key(Provider.GROQ,db,user)
    client = Groq(api_key=api_key)


    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Use "llama3-8b" if you need LLaMA 3
        messages=[
            {"role": "system", "content": "You are a Professional Html Designer and Content Creator/Writer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    
    return response.choices[0].message.content
    
def get_answer_to_query(prompt: str,db : Session,user : User) -> str:

    # Initialize the Groq client
    api_key =  get_api_key(Provider.GROQ,db,user)
    client = Groq(api_key=api_key)
    
    response = client.chat.completions.create(
        model="llama3-70b-8192",  # Use "llama3-8b" if you need LLaMA 3
        messages=[
            {"role": "system", "content": "You are a Helpful AI Assistant"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    
    return response.choices[0].message.content