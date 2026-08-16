from uvicorn import Config, Server
from discord import Embed, Colour
from datetime import datetime
from lib.logger import logger
from fastapi import FastAPI
from os import getenv
from bot import bot
app = FastAPI()

@app.post("/github/push")
async def push(data: dict):
    logger.info("New request on push method", extra={"file": "server.py"})

    repo_url, repo_id, repo_name = data["repository"]["html_url"], data["repository"]["id"], data["repository"]["name"]
    commit_list = data["commits"]

    if len(commit_list) < 1:
        logger.debug("No commit on the push", extra={"file": "server.py"})
        return {"status": "ok"}

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
    logger.info(f"Sucessfully push commits info on {getenv("CHANNEL_MESSAGE_ID")}", extra={"file": "server.py"})

    return {"status": "ok"}

@app.post("/github/tags")
async def tags(data: dict):
    logger.info("New request on tag method", extra={"file": "server.py"})

    ref_type = data["ref_type"]
    if ref_type != "tag":
        logger.warning("No ref_type to tag", extra={"file": "server.py"})
        return {"status": "nok"}

    tag_name = data["ref"]
    tag_branch = data["master_branch"]
    user_pusher = data["pusher_type"]
    repo_url, repo_id, repo_name = data["repository"]["html_url"], data["repository"]["id"], data["repository"]["name"]

    avatar = f"https://avatars.githubusercontent.com/u/{data["sender"]["id"]}?v=4"
    repo_infos = f"""Repository Informations:
Repository URl: {repo_url}
Repository ID: {repo_id}
Pushed by: {data["sender"]["login"]}
    """
    
    embed_tags = Embed(
        title=f"[NEW TAG] - {repo_name}",
        description=repo_infos,
        color=Colour.blue()
    )
    
    tag_infos =  f"""Tag Name: ``{tag_name}``
Tag Branch: {tag_branch}
Taged by: {data["sender"]["login"]} - {"Utilisateur" if user_pusher == "user" else data["pusher_type"]}
"""
    embed_tags.add_field(name=f"{tag_name}", value=tag_infos)

    embed_tags.set_author(name=f"Sender Commit - {data["sender"]["login"]}", icon_url=avatar)
    embed_tags.set_thumbnail(url=f"https://opengraph.githubassets.com/1/{data["repository"]["owner"]["login"]}/{repo_name}")
    embed_tags.set_footer(text=f"{str(datetime.now()).split('.')[0]}")

    channel = bot.get_channel(int(getenv("CHANNEL_MESSAGE_ID")))
    await channel.send(embed=embed_tags)
    logger.info(f"Sucessfully push commits info on {getenv("CHANNEL_MESSAGE_ID")}", extra={"file": "server.py"})

    return {"status": "ok"}

@app.post("/")
async def root(req: dict):
    print(req)
    return {"status": "ok"}

async def start_server():
    logger.info("Starting FastAPI Server", extra={"file": "server.py"})

    config = Config(
        app,
        host="0.0.0.0",
        port=int(getenv("LISTENING_FASTAPI_PORT")),
        log_config=None
    )
    server = Server(config)
    await server.serve()

