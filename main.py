import asyncio
import logging
import os
import json
import random
from typing import Dict
from datetime import datetime #
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import aioschedule as schedule load_dotenvBOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607995788"))
loops_db: Dict[str, dict] = {} logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage) class LoopStates(StatesGroup): waiting_seconds = Statewaiting_message = Statedef save_loops: with open("loops.json", "w") as f: json.dump(loops_db, f, indent=2) def load_loops: global loops_db try: with open("loops.json", "r") as f: loops_db.update(json.load(f)) except: pass def get_main_kb(is_admin=False): kb = InlineKeyboardMarkup(inline_keyboard=[ [InlineKeyboardButton(text="🔄 Criar Loop", callback_data="create_loop")], [InlineKeyboardButton(text="📊 Status", callback_data="status")], [InlineKeyboardButton(text="🛑 Parar", callback_data="stop")] ]) if is_admin: kb.inline_keyboard.append([InlineKeyboardButton(text="👑 Admin", callback_data="admin")]) return kb async def run_loop(chat_id: str): while loops_db[chat_id]["active"]: try: text = loops_db[chat_id]["text"] if '|' in text: texts = [t.stripfor t in text.split('|')] text = random.choice(texts) await bot.send_message(int(chat_id), text) await asyncio.sleep(loops_db[chat_id]["seconds"]) except Exception as e: logging.error(f"Erro loop {chat_id}: {e}") break @dp.message(Command("start"))
async def start(message: Message): load_loopskb = get_main_kb(message.from_user.id == ADMIN_ID) await message.answer("🚀 **LoopBot PRO v3.0** ATIVO!\nCrie loops infinitos:", reply_markup=kb) @dp.message(LoopStates.waiting_seconds)
async def set_seconds(message: Message, state: FSMContext): try: seconds = int(message.text) if seconds < 3: return await message.answer("❌ Mínimo 3 segundos!") await state.update_data(seconds=seconds) await message.answer(f"✅ {seconds}s OK!\n\n📝 **Mensagem** (use | pra random):") await state.set_state(LoopStates.waiting_message) except: await message.answer("❌ Digite só números!") @dp.message(LoopStates.waiting_message)
async def set_message(message: Message, state: FSMContext): data = await state.get_datachat_id = str(message.chat.id) loops_db[chat_id] = { "seconds": data["seconds"], "text": message.text, "active": True, "randomize": '|' in message.text, "created": datetime.now.isoformat} save_loopsawait message.answer(f"🔥 **LOOP ATIVO!**\n⏱️ {data['seconds']}s\n📄 `{message.text}`", reply_markup=get_main_kb(message.from_user.id == ADMIN_ID)) asyncio.create_task(run_loop(chat_id)) await state.clear@dp.callback_query(F.data == "create_loop")
async def create_loop_cb(callback: CallbackQuery, state: FSMContext): await callback.message.edit_text("⏱️ **Digite os segundos** (mín 3):") await state.set_state(LoopStates.waiting_seconds) await callback.answerasync def main: load_loopsawait dp.start_polling(bot) if __name__ == "__main__": asyncio.run(main)
