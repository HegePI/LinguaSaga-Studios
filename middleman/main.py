from fastapi import FastAPI
from pydantic import BaseModel

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
    return {"message": "Hello world"}

@app.post("/conversation")
def post_conversation(payload: Payload):
    return {"response": payload.npc_name}