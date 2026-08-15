from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
import discord
load_dotenv()

_PREFIX = str(getenv("PREFIX")).strip()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix=_PREFIX, intents=intents)

@bot.command(name="test")
async def test(ctx):
    await ctx.send("test")

@bot.event
async def on_ready():
    assert bot.user is not None
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.event
async def on_message(message):
    content = message.content
    
    if content.count(_PREFIX) > 0 and content[:len(_PREFIX)] == _PREFIX:
        await bot.process_commands(message)
        return
    
    print(message)

async def start_bot():
    await bot.start(getenv("TOKEN"))