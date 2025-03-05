from fastapi import WebSocket, WebSocketDisconnect


class WebSocketManager:
    """Class quản lý tất cả WebSocket clients."""

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Kết nối client mới."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Ngắt kết nối client."""
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Gửi tin nhắn đến tất cả WebSocket clients."""
        for connection in self.active_connections:
            await connection.send_text(message)
