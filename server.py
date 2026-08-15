from uvicorn import Config, Server
from fastapi import FastAPI
from bot import bot
app = FastAPI()

@app.post("/github/push")
async def push(data: dict):
    repo_url, repo_id = data["repository"]["html_url"], data["repository"]["id"]
    forced_push = data["forced"]
    
    channel = bot.get_channel(1535661127185469503)
    await channel.send("test")
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

