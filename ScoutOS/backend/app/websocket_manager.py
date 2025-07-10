from typing import Dict, List
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(user_id, []).append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        connections = self.active_connections.get(user_id, [])
        try:
            connections.remove(websocket)
            if not connections:
                self.active_connections.pop(user_id, None)
        except ValueError:
            pass

    async def send_personal_message(self, message: str, user_id: str):
        connections = self.active_connections.get(user_id, [])
        for connection in connections:
            await connection.send_text(message)

    async def broadcast(self, message: str):
        for user_connections in self.active_connections.values():
            for connection in user_connections:
                await connection.send_text(message)


manager = ConnectionManager()
