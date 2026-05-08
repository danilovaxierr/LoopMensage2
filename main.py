import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import aioschedule
from datetime import datetime load_dotenvTOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = int(os.getenv("TARGET_CHAT_ID", "-1001234567890"))
MESSAGES = ["💎 Loop 1", "🔥 Loop 2", "🚀 Loop 3"] logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher@dp.message(Command("start"))
async def start(msg: Message): await msg.answer("🚀 **LoopBot v4 UP!** /loop") @dp.message(Command("loop"))
async def loop(msg: Message): await msg.answer("🔄 **Loops ON!** /stop") asyncio.create_task(run_scheduler) async def send_message: try: msg = MESSAGES[datetime.now.minute % 3] await bot.send_message(chat_id=TARGET_CHAT_ID, text=msg) logging.info("✅ Msg enviada!") except Exception as e: logging.error(f"❌ Erro: {e}") async def run_scheduler: aioschedule.every(5).minutes.do(send_message) while True: aioschedule.run_pendingawait asyncio.sleep(1) @dp.message(Command("stop"))
async def stop(msg: Message): aioschedule.clearawait msg.answer("⏹️ **Loops OFF!**") async def main: await dp.start_polling(bot) if __name__ == "__main__": asyncio.run(main)
