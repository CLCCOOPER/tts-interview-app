import os
from io import BytesIO

import requests
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from voice_manager import get_voice_id

load_dotenv()  # loads .env
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

app = FastAPI(title="TTS backend")

class TTSRequest(BaseModel):
    text: str
    voice_name: str | None = "default"   # optional override

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

    r = requests.post(url, json=payload, headers=headers, timeout=40)
    if r.status_code != 200:
        raise HTTPException(status_code=r.status_code,
                            detail=r.json().get("detail", "ElevenLabs error"))

    return StreamingResponse(BytesIO(r.content), media_type="audio/mpeg")

