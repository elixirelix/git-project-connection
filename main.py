from asyncio import gather, run
from server import start_server
from bot import start_bot

async def main():
    await gather(
        start_server(),
        start_bot()
    )

if __name__ == "__main__":
    run(main())