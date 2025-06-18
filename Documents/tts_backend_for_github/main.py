import os
from io import BytesIO

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from voice_manager import get_voice_id

# Load environment variables
load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

# Initialize FastAPI app
app = FastAPI(title="TTS backend")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origin(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class TTSRequest(BaseModel):
    text: str
    voice_name: str | None = "default"  # Optional voice override

# Root route (health check)
@app.get("/")
def read_root():
    return {"message": "TTS API is live"}

# TTS generation route
@app.post("/generate-audio")
def generate_audio(req: TTSRequest):
    voice_id = get_voice_id(req.voice_name)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {
        "text": req.text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
    }

    try:
        r = requests.post(url, json=payload, headers=headers, timeout=40)
        r.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

    return StreamingResponse(BytesIO(r.content), media_type="audio/mpeg")
