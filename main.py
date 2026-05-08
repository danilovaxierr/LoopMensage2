import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenvload_dotenvTOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher@dp.message(Command("start"))
async def start(msg: Message): await msg.answer("🚀 LoopBot v3.0 OK!")async def main: await dp.start_polling(bot)if __name__ == "__main__": asyncio.run(main)
