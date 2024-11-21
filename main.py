from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import uvicorn


app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections = []
        self.usernames: dict[WebSocket, str] = {}

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        await self.broadcast(f"{username} joined chat", sender=websocket)
        self.active_connections.append(websocket)
        self.usernames[websocket] = username

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            username = self.usernames.get(websocket)
            self.active_connections.remove(websocket)
            del self.usernames[websocket]
            return username

    async def broadcast(self, message: str, sender: WebSocket = None):
        for connection in self.active_connections:
            if connection != sender:
                await connection.send_text(message)


manager = ConnectionManager()


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{username}: {data}", sender=websocket)
    except WebSocketDisconnect:
        username = manager.disconnect(websocket)
        await manager.broadcast(f"{username} left chat", sender=websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
