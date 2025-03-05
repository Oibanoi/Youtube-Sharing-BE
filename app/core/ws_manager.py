from fastapi import WebSocket, WebSocketDisconnect


class WebSocketManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        # Dù gọi __new__ chỉ một lần, __init__ vẫn có thể được gọi nếu cần thiết
        if not hasattr(self, 'active_connections'):
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
            try:
                print("seding")
                await connection.send_text(message)
            except Exception as e:
                print(f"Error sending message: {e}")
                self.disconnect(connection)
