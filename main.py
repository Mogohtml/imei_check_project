import asyncio
from app.bot import main as bot_main
from app.api import app as api_app

async def run_bot():
    await bot_main()

async def run_api():
    api_app.run(debug=True, use_reloader=False)

async def main():
    bot_task = asyncio.create_task(run_bot())
    api_task = asyncio.create_task(run_api())
    await asyncio.gather(bot_task, api_task)

if __name__ == '__main__':
    asyncio.run(main())
