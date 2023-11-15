from fastapi import WebSocket, WebSocketDisconnect

from middleman.models.llm_model import HugginfaceInferenceClientStreamingCustomLLM
from middleman.utils.ConnectionManager import ConnectionManager


class ConversationManager:
    def __init__(
        self,
        websocket: WebSocket,
        connection_manager: ConnectionManager,
        llm: HugginfaceInferenceClientStreamingCustomLLM,
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
                for chunk in self.llm.stream(prompt=data["player_input"]):
                    print("chunk: ", chunk)
                    await self.websocket.send_text(chunk)

        except WebSocketDisconnect:
            self.connection_manager.disconnect(self.websocket)
