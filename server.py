from fastapi import FastAPI, Request
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


