from fastapi import APIRouter
from starlette.websockets import WebSocket, WebSocketDisconnect

from app.core.ws_manager import WebSocketManager
from app.schemas.sche_base import ResponseSchemaBase

router = APIRouter()

ws_manager= WebSocketManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Giữ kết nối mở
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)