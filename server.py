from fastapi import FastAPI
from uvicorn import Config, Server
app = FastAPI()

@app.post("/github/push")
async def push(data: dict):
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/")
async def root(req: dict):
    print(req)
    return {"status": "ok"}

async def start_server():
    config = Config(
        app,
        host="0.0.0.0",
        port=8000
    )
    server = Server(config)
    await server.serve()

