from voice_manager import get_voice_id

@app.post("/generate-audio")
def generate_audio(req: TTSRequest):
    voice_id = get_voice_id("female_soft")  # You can pass any label from your voice_manager.py

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

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to generate audio."
        )

    return StreamingResponse(BytesIO(response.content), media_type="audio/mpeg")
