from fastapi import WebSocket, WebSocketDisconnect

from ConnectionManager import ConnectionManager
from models.llm_model import HugginfaceInferenceClientStreamingCustomLLM

from langchain.llms.base import LLM


class ConversationManager:
    def __init__(
        self, websocket: WebSocket, connection_manager: ConnectionManager, llm: LLM
    ) -> None:
        self.websocket = websocket
        self.connection_manager = connection_manager
        self.llm = llm

    async def connect_to_websocket(self):
        await self.connection_manager.connect(websocket=self.websocket)

    async def start_conversation(self):
        try:
            while True:
                data = await self.websocket.receive_json()
                self.llm(prompt=data["player_input"])
                for chunk in self.llm.streamer:
                    await self.websocket.send_text(chunk)
        except WebSocketDisconnect:
            self.connection_manager.disconnect(self.websocket)
