from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from io import BytesIO

# Load environment variables from .env
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Get API key and set voice ID
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # You can replace with your custom voice ID

# Define input model
class TTSRequest(BaseModel):
    text: str

# Health check endpoint
@app.get("/")
def read_root():
    return {"message": "TTS API is live"}

# Text-to-speech generation endpoint
@app.post("/generate-audio")
def generate_audio(req: TTSRequest):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    payload = {
        "text": req.text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(status_code_
