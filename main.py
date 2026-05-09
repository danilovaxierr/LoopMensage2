import asyncio
import os
import logging
from datetime import datetime

import aioschedule
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID", "-1001234567890"))

MESSAGES = [
    "💎 Loop 1",
    "🔥 Loop 2",
    "🚀 Loop 3"
]

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

scheduler_task = None


@dp.message(Command("start"))
async def start(msg: Message):
    await msg.answer("🚀 LoopBot v4 UP! Use /loop")


async def send_message():
    try:
        index = datetime.now().minute % len(MESSAGES)
        text = MESSAGES[index]

        await bot.send_message(
            chat_id=TARGET_CHAT_ID,
            text=text
        )

        logging.info("✅ Msg enviada!")

    except Exception as e:
        logging.error(f"❌ Erro: {e}")


async def run_scheduler():
    aioschedule.every(5).minutes.do(send_message)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


@dp.message(Command("loop"))
async def loop(msg: Message):
    global scheduler_task

    if scheduler_task is None or scheduler_task.done():
        scheduler_task = asyncio.create_task(run_scheduler())
        await msg.answer("🔄 Loops ON! Use /stop")
    else:
        await msg.answer("⚠️ O loop já está ligado.")


@dp.message(Command("stop"))
async def stop(msg: Message):
    global scheduler_task

    aioschedule.clear()

    if scheduler_task:
        scheduler_task.cancel()
        scheduler_task = None

    await msg.answer("⏹️ Loops OFF!")


async def health(request):
    return web.Response(text="Bot online!")


async def start_webserver():
    app = web.Application()
    app.router.add_get("/", health)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", 10000))

    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    logging.info(f"🌐 Web server rodando na porta {port}")


async def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN não encontrado no .env")

    await start_webserver()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
