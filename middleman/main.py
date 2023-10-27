from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.llms import HuggingFaceHub
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.prompts import (
    MessagesPlaceholder,
    HumanMessagePromptTemplate,
)
from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema import SystemMessage
from langchain.chains import LLMChain


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


@app.post("/conversation")
def post_conversation(payload: Payload):
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
