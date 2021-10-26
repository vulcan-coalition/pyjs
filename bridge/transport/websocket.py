from fastapi import WebSocket, WebSocketDisconnect
from typing import List
from functools import partial
import asyncio


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.id_2_client = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, data):
        for connection in self.active_connections:
            await connection.send_json(data)


manager = ConnectionManager()


def init(app, get_active_client_class, on_receive_msg):
    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        await manager.connect(websocket)
        # transport is the socket.
        client_obj = get_active_client_class()(websocket)
        try:
            while True:
                package = await websocket.receive_json()
                on_receive_msg(client_obj, package["f"], [], package["d"])
        except WebSocketDisconnect:
            manager.disconnect(websocket)


def send_data(websocket, function_call, kwargs):
    package = {
        "f": function_call,
        "d": kwargs
    }

    asyncio.ensure_future(partial(websocket.send_json, package)())
