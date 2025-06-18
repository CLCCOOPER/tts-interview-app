import httpx
import os
from dotenv import load_dotenv

# Load the ElevenLabs API key
load_dotenv()
api_key = os.getenv("ELEVEN_API_KEY")
print(f"🔐 Loaded API Key: {api_key}")

url = "https://tts-interview-app-1.onrender.com/generate-audio"
payload = {"text": "This is a test using httpx!"}
headers = {"Content-Type": "application/json"}

try:
    response = httpx.post(url, json=payload, headers=headers, timeout=30.0)
    if response.status_code == 200:
        with open("output_test_httpx.mp3", "wb") as f:
            f.write(response.content)
        print("✅ Audio file saved as output_test_httpx.mp3")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
except httpx.RequestError as e:
    print(f"❌ Network error: {e}")
