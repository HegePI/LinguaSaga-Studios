import os

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chat_models.openai import ChatOpenAI
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.prompts import (
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
)
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import SystemMessage
from pydantic import BaseModel
from utils.ConnectionManager import ConnectionManager
from vectorstore import load_index, query_index

load_dotenv()

app = FastAPI()


class Task(BaseModel):
    description: str


class NPCData(BaseModel):
    npc_name: str
    backstory: str
    description: str
    tasks: list[Task]


class Payload(BaseModel):
    player_name: str
    player_input: str
    npc_data: NPCData


# Load index assuming it exists
INDEX = load_index(os.environ["INDEX_NAME"])

LLM = ChatOpenAI()

CONNECTION_MANAGER = ConnectionManager()


@app.get("/")
def root():
    return {"version": "0.0.1"}


@app.post("/conversation")
def post_conversation(payload: Payload):
    print(payload)
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=f"You are impersonating a NPC called {payload.npc_data.npc_name} that is described as {payload.npc_data.description}. Imitate this character to best of you ability, but in case of you do not know what to say, say something agressive."
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    # llm = ChatOpenAI(temperature=0)

    llm = HuggingFaceHub(
        repo_id="google/flan-t5-xxl",
        model_kwargs={"temperature": 0.5, "max_length": 64},
    )

    chat_chain = LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)

    return {
        "response": chat_chain.predict(
            human_input=payload.player_input,
        )
    }


@app.post("/conversation/stream")
async def post_conversation_stream(payload: Payload):
    print("conversation/stream")
    generator = LLM.stream(payload.player_input)
    return StreamingResponse((line for line in generator), media_type="text/plain")


@app.websocket("/ws/conversation/npc1")
async def conversation(websocket: WebSocket):
    chain = None

    await CONNECTION_MANAGER.connect(websocket)
    try:
        while True:
            data: Payload = await websocket.receive_json()

            if chain is None:
                chain = get_chain(data)

            context = query_index(INDEX, data["player_input"])
            response = chain({"human_input": data["player_input"], "context": context})
            await CONNECTION_MANAGER.send_message(response["text"], websocket)
    except WebSocketDisconnect:
        CONNECTION_MANAGER.disconnect(websocket)


@app.websocket("/ws/conversation/npc2")
async def conversation(websocket: WebSocket):
    chain = None

    await CONNECTION_MANAGER.connect(websocket)
    try:
        while True:
            data: Payload = await websocket.receive_json()

            if chain is None:
                chain = get_chain(data)

            context = query_index(INDEX, data["player_input"])
            response = chain({"human_input": data["player_input"], "context": context})
            await CONNECTION_MANAGER.send_message(response["text"], websocket)
    except WebSocketDisconnect:
        CONNECTION_MANAGER.disconnect(websocket)


def get_chain(data: Payload):
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content=f"""You are a NPC character from the world of cyberpunk and you are having a conversation with a player.
            You are impersonating a NPC called {data["npc_data"]["npc_name"]}.
            You are described as {data["npc_data"]["description"]}.
            Your tasks to the player are {", ".join(d["description"] for d in data["npc_data"]["tasks"])} and you reveal them to the player if player asks about them.
            If player writes that he is willing to do the task, write in the end of the reponse <MISSION_INITIATED>.
            Imitate this character to best of you ability, but in case of you do not know what to say, say something agressive."""
            ),
            SystemMessagePromptTemplate.from_template("Context: {context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="human_input",
        return_messages=True,
    )

    chain = LLMChain(
        prompt=prompt,
        llm=LLM,
        memory=memory,
        verbose=True,
    )

    return chain
