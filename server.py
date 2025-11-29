from fastapi import FastAPI, WebSocket
from app import encrypt, decrypt
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()
viewers = []

@app.websocket("/stream")
async def agent_stream(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            encrypted = await ws.receive_bytes()
            frame = decrypt(encrypted)

            for viewer in viewers:
                try:
                    await viewer.send_bytes(frame)
                except:
                    pass
    except:
        pass


@app.websocket("/view")
async def view(ws: WebSocket):
    await ws.accept()
    viewers.append(ws)

    try:
        while True:
            await ws.receive_text()
    except:
        viewers.remove(ws)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000)
