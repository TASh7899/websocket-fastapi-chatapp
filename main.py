from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware #cross origin resourse sharing
from typing import Dict
from datetime import datetime
import json

#dictornary
connected_user : Dict[str, WebSocket]={}
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(user_id: str, websocket: WebSocket ):

    await websocket.accept()
    connected_user[user_id] = websocket

    try:
        while True:
            data = await websocket.receive_text()
            for user, user_ws in connected_user.items():
                await user_ws.send_text(data)
    except WebSocketDisconnect:
        print(f"user {user_id} disconnected")
        del connected_user[user_id]
        await websocket.close()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)






