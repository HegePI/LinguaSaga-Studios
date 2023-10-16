from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json
import os

load_dotenv()

API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
API_TOKEN = os.getenv("API_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

app = FastAPI()

class Task(BaseModel):
    description: str

class Data(BaseModel):
    backstory: str
    description: str
    tasks: list[Task]

class Payload(BaseModel):
    npc_name: str
    user_prompt: str
    npc_data: Data

@app.get("/")
def root():
    return {"version": "0.0.1"}

@app.post("/conversation")
def post_conversation(payload: Payload):
    data = json.dumps({
        "inputs": {
            "text": payload.user_prompt
        },
        "options": {
            "wait_for_model": True
        }
    })
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return {"res": json.loads(response.content.decode("utf-8"))}