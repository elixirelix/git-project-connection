from uvicorn import Config, Server
from fastapi import FastAPI
from discord import Embed, Colour
from os import getenv
from bot import bot
app = FastAPI()

@app.post("/github/push")
async def push(data: dict):
    repo_url, repo_id, repo_name = data["repository"]["html_url"], data["repository"]["id"], data["repository"]["name"]
    commit_list = data["commits"]
    
    if len(commit_list) < 1: return {"status": "ok"}

    avatar = f"https://avatars.githubusercontent.com/u/{data["sender"]["id"]}?v=4"
    repo_infos = f"""Repository Informations:
Repository URl: {repo_url}
Repository ID: {repo_id}
Total Commit: {len(commit_list)}
Pushed by: {data["sender"]["login"]}
    """
    
    embed_push = Embed(
        title=f"[NEW PUSH] - {repo_name}",
        description=repo_infos,
        color=Colour.blue()
    )
    
    for commits in commit_list:
        commit_id, commit_message = commits["id"], commits["message"]
        commit_add, commit_remove, commit_modified = commits["added"], commits["removed"], commits["modified"]
        commit_infos =  f"""Files edited: {len(commit_add) + len(commit_remove) + len(commit_modified)}
Add: {"``" + "`` ``".join(commit_add) + "``" if len(commit_add) > 0 else "No files"}
Modified: {"``" + "`` ``".join(commit_modified) + "``" if len(commit_modified) > 0 else "No files"}
Remove: {"``" + "`` ``".join(commit_remove) + "``" if len(commit_remove) > 0 else "No files"}

Message: ``{commits["message"]}``
Commit time: {commits["timestamp"]}
Commited by: {commits["committer"]["name"]}
"""

        embed_push.add_field(name=f"{commit_message} - {commit_id}", value=commit_infos)

    embed_push.set_author(name=f"Sender Commit - {data["sender"]["login"]}", icon_url=avatar)
    embed_push.set_thumbnail(url=f"https://opengraph.githubassets.com/1/{data["repository"]["owner"]["login"]}/{repo_name}")
    embed_push.set_footer(text=f"{data["head_commit"]["timestamp"]}")

    channel = bot.get_channel(int(getenv("CHANNEL_MESSAGE_ID")))
    await channel.send(embed=embed_push)

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
        port=8000,
        log_config=None
    )
    server = Server(config)
    await server.serve()

