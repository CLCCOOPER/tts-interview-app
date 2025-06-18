from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests, os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from io import BytesIO
from VOICE_ID import VOICE_ID  # importing the voice ID

load_dotenv()
app = FastAPI()

ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")

class TTSRequest(BaseModel):
    text: str

@app.get("/")
def read_root():
    return {"message": "TTS API is live"}

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
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5}
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to generate audio."
        )

    return StreamingResponse(BytesIO(response.content), media_type="audio/mpeg")
