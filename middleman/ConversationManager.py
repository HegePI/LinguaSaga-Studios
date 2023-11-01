from fastapi import WebSocket, WebSocketDisconnect
from middleman.ConnectionManager import ConnectionManager
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.llms.base import LLM

from langchain.llms.huggingface_pipeline import HuggingFacePipeline

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


class ConversationManager:
    def __init__(
        self, websocket: WebSocket, connection_manager: ConnectionManager
    ) -> None:
        self.websocket = websocket
        self.connection_manager = connection_manager
        self.conversation_buffer_memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.conversation_chain = LLMChain(
            llm=self.llm,
            verbose=True,
            memory=self.conversation_buffer_memory,
        )

        model_id = "bigscience/bloom"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id)
        pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    async def connect_to_websocket(self):
        await self.connection_manager.connect(websocket=self.websocket)

    async def start_conversation(self):
        try:
            while True:
                data = await self.websocket.receive_json()
                self.conversation_chain.predict()
        except WebSocketDisconnect:
            self.connection_manager.disconnect(self.websocket)
