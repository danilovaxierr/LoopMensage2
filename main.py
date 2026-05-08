import asyncio
import logging
import os
import json
import random
from typing import Dict
from datetime import datetime
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aioschedule as schedule
from dotenv import load_dotenv load_dotenv# Config
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "8607995788"))
loops_db: Dict[str, dict] = {}
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage)
router = Routerdp.include_router(router) class LoopStates(StatesGroup): waiting_seconds = Statewaiting_message = Statedef save_loops: with open("loops.json", "w") as f: json.dump(loops_db, f, indent=2) def load_loops: global loops_db try: with open("loops.json", "r") as f: loops_db.update(json.load(f)) except: pass def get_main_kb(is_admin=False): kb = InlineKeyboardMarkup(inline_keyboard=[ [InlineKeyboardButton(text="🔄 Criar Loop", callback_data="create_loop")], [InlineKeyboardButton(text="📊 Status", callback_data="status")], [InlineKeyboardButton(text="🛑 Parar", callback_data="stop")], [InlineKeyboardButton(text="⚡️ Boost", callback_data="boost")] ]) if is_admin: kb.inline_keyboard.append([InlineKeyboardButton(text="👑 Admin", callback_data="admin_panel")]) return kb async def run_loop(chat_id: str): while loops_db[chat_id]["active"]: try: text = loops_db[chat_id]["text"] if loops_db[chat_id].get("randomize", False): text = random.choice(text.split('|')) await bot.send_message(int(chat_id), text) await asyncio.sleep(loops_db[chat_id]["seconds"]) except: break .message(Command("start"))
async def start(message: Message): load_loopskb = get_main_kb(message.from_user.id == ADMIN_ID) await message.answer("🚀 **LoopBot PRO v3.0** online!\n\nUse os botões:", reply_markup=kb) .message(LoopStates.waiting_seconds)
async def set_seconds(message: Message, state: FSMContext): try: seconds = int(message.text) if seconds < 3: return await message.answer("❌ Mínimo 3 segundos!") await state.update_data(seconds=seconds) await message.answer(f"✅ {seconds}s ok!\n\n📝 Agora a mensagem (use | pra random):") await state.set_state(LoopStates.waiting_message) except: await message.answer("❌ Só números!") .message(LoopStates.waiting_message)
async def set_message(message: Message, state: FSMContext): data = await state.get_datachat_id = str(message.chat.id) loops_db[chat_id] = { "seconds": data["seconds"], "text": message.text, "active": True, "randomize": "|" in message.text, "created": datetime.now.isoformat} save_loopsawait message.answer(f"🔥 **LOOP ATIVO!**\n\n⏱️ {data['seconds']}s\n📄 `{message.text}`", reply_markup=get_main_kb(message.from_user.id == ADMIN_ID)) asyncio.create_task(run_loop(chat_id)) await state.clear.callback_query(F.data == "create_loop")
async def create_loop(callback: CallbackQuery, state: FSMContext): await callback.message.edit_text("⏱️ Digite os **segundos** (mín 3):") await state.set_state(LoopStates.waiting_seconds) await callback.answer# Outros handlers aqui (status, stop, admin)...
async def main: load_loopsawait dp.start_polling(bot) if __name__ == "__main__": asyncio.run(main)
