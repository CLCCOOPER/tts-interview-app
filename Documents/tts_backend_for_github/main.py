from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
from io import BytesIO

load_dotenv()

app = FastAPI()

# 👇 Add this
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, use your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
