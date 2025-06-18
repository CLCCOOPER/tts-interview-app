import os
from io import BytesIO

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import requests

from voice_manager import get_voice_id

# ── ENV ──────────────────────────────────────────────────────────────────────
load_dotenv()
ELEVEN_API_KEY = os.getenv("ELEVEN_API_KEY")
if not ELEVEN_API_KEY:
    raise RuntimeError("ELEVEN_API_KEY missing – add it to .env")

# ── APP ──────────────────────────────────────────────────────────────────────
app = FastAPI(title="TTS-backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # ⚠️  tighten in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── MODEL ────────────────────────────────────────────────────────────────────
class TTSRequest(BaseModel):
    text: str
    voice_name: str | None = "default"

# ── ROUTES ───────────────────────────────────────────────────────────────────
@app.get("/")
def ping() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/generate-audio")
def generate_audio(req: TTSRequest):
    voice_id = get_voice_id(req.voice_name)
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": req.text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.5},
    }

    resp = requests.post(url, json=payload, headers=headers, timeout=40)
    if resp.status_code != 200:
        detail = resp.json().get("detail", resp.text)
        raise HTTPException(status_code=resp.status_code, detail=detail)

    return StreamingResponse(BytesIO(resp.content), media_type="audio/mpeg")
