import json
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, session_id: int):
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = []
        self.active_connections[session_id].append(websocket)

    def disconnect(self, websocket: WebSocket, session_id: int):
        if session_id in self.active_connections:
            if websocket in self.active_connections[session_id]:
                self.active_connections[session_id].remove(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]

    async def send_json(self, websocket: WebSocket, data: dict):
        """Send to a single connection."""
        try:
            await websocket.send_json(data)
        except Exception:
            pass

    async def broadcast(self, session_id: int, data: dict, exclude: WebSocket | None = None):
        """Send to all connections in a session, optionally excluding one."""
        if session_id in self.active_connections:
            for connection in list(self.active_connections[session_id]):
                if connection is exclude:
                    continue
                try:
                    await connection.send_json(data)
                except Exception:
                    pass

    async def broadcast_all(self, session_id: int, data: dict):
        """Send to ALL connections in a session (including sender)."""
        if session_id in self.active_connections:
            for connection in list(self.active_connections[session_id]):
                try:
                    await connection.send_json(data)
                except Exception:
                    pass


manager = ConnectionManager()
