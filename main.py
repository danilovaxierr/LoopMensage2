import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
import aioschedule
from datetime import datetime load_dotenvTOKEN = os.getenv("BOT_TOKEN")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID") # ID do grupo
MESSAGES = ["💎 Mensagem 1", "🔥 Mensagem 2", "🚀 Mensagem 3"] logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher@dp.message(Command("start"))
async def start(msg: Message): await msg.answer("🚀 **LoopBot v3.0 ATIVO!**\n📱 Envie /loop para ativar loops") @dp.message(Command("loop"))
async def loop(msg: Message): await msg.answer("🔄 **Loops ativos!** Parar: /stop") aioschedule.every(5).minutes.do(send_message) asyncio.create_task(run_scheduler) async def send_message: try: await bot.send_message(chat_id=TARGET_CHAT_ID, text=MESSAGES[datetime.now.minute % 3]) logging.info("Mensagem enviada!") except Exception as e: logging.error(f"Erro: {e}") async def run_scheduler: while True: aioschedule.run_pendingawait asyncio.sleep(1) @dp.message(Command("stop"))
async def stop(msg: Message): aioschedule.clearawait msg.answer("⏹️ **Loops parados!**") async def main: await dp.start_polling(bot) if __name__ == "__main__": asyncio.run(main)
