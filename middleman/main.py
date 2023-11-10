from ConnectionManager import ConnectionManager
from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from langchain.chains import LLMChain
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms.huggingface_hub import HuggingFaceHub
from langchain.prompts import HumanMessagePromptTemplate, MessagesPlaceholder
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import SystemMessage
from models.llm_model import HugginfaceInferenceClientStreamingCustomLLM
from pydantic import BaseModel

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


@app.get("/")
def root():
    return {"version": "0.0.1"}


connection_manager = ConnectionManager()

llm = HugginfaceInferenceClientStreamingCustomLLM()


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
    generator = llm.stream_answer(payload.player_input)
    return StreamingResponse((line for line in generator), media_type="text/plain")


@app.websocket("/ws/conversation")
async def conversation(websocket: WebSocket):
    await connection_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            for chunk in llm.stream_answer(data["player_input"]):
                await connection_manager.send_message(chunk, websocket)
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
