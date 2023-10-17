from dotenv import load_dotenv
from fastapi import FastAPI
from langchain import ConversationChain
from pydantic import BaseModel
from langchain.llms import HuggingFaceHub
from langchain.chains.conversation.memory import ConversationBufferMemory


load_dotenv()

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
    repo_id = "bigscience/bloom"
    llm = HuggingFaceHub(
        repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
    )
    conversation = ConversationChain(
        llm=llm, verbose=True, memory=ConversationBufferMemory()
    )

    return {"response": conversation.predict(input=payload.user_prompt)}
