from asyncio import gather, run
from server import start_server
from dotenv import load_dotenv
from bot import start_bot
load_dotenv()

async def main():
    await gather(
        start_server(),
        start_bot()
    )

if __name__ == "__main__":
    run(main())