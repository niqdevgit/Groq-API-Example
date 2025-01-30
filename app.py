from fastapi import FastAPI
import requests
import os
from dotenv import load_dotenv
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# Fetch the API Key from the .env file
API_KEY = os.getenv('GROQ_API_KEY')  # Replace with your API key variable name
BASE_URL = "https://api.x.ai/v1/chat/completions"

app = FastAPI()

class TranslationRequest(BaseModel):
    text: str
    target_lang: str

@app.post("/translate")
async def translate(request: TranslationRequest):
    # Sending the translation request to the Groq API
    response = requests.post(
        BASE_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={
            "text": request.text,
            "target_lang": request.target_lang
        }
    )

    if response.status_code == 200:
        translation = response.json().get("translatedText")
        return {"translatedText": translation}
    else:
        return {"error": "Translation failed", "status_code": response.status_code}

