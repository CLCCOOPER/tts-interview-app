import httpx
import os
from dotenv import load_dotenv

# Load the ELEVEN_API_KEY from your .env file
load_dotenv()
api_key = os.getenv("ELEVEN_API_KEY")

url = "https://tts-interview-app-1.onrender.com/generate-audio"
payload = {"text": "This is a test using httpx!"}
headers = {
    "Content-Type": "application/json",
    "xi-api-key": api_key  # This is required for authentication
}

try:
    response = httpx.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        with open("output_test_httpx.mp3", "wb") as f:
            f.write(response.content)
        print("✅ Audio file saved as output_test_httpx.mp3")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
except httpx.RequestError as e:
    print(f"❌ Network error: {e}")
