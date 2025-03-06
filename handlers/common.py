from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from handlers.post import clear_ids

from config import ADMIN_IDS
from keyboards.common import main_menu_keyboard, transport_or_cargo_keyboard
from utils.data_manager import DataManager


async def start(message: types.Message, state: FSMContext):
  user_manager = DataManager("users.json")
  user_id = str(message.from_user.id)
  if user_manager.get_by_id(user_id):
    await message.answer("Botga xush kelibsiz!\nIltimos kerakli amalni tanlang:", reply_markup=main_menu_keyboard())
    return

  await state.set_state("register:phone")
  await message.answer("Iltimos raqamingizni ulashing:", reply_markup=types.ReplyKeyboardMarkup(keyboard=[[types.KeyboardButton(text="Raqamni berish 📞", request_contact=True)]], resize_keyboard=True))


async def back(message: types.Message, state: FSMContext):
  await state.clear()
  await clear_ids(message.from_user.id)
  await message.answer("Asosiy menuga qaytildi", reply_markup=main_menu_keyboard())


async def select_transport_or_cargo(message: types.Message, state: FSMContext):
    if message.text == "E'lon berish":
        await state.set_state("post:select_type")
        await message.answer("Nimani e'lon qilmoqchisiz?", reply_markup=transport_or_cargo_keyboard())

    elif message.text == "Qidirish":
       await state.set_state("search:cargo_name")
       await message.answer("Nimani qidirmoqchisiz?", reply_markup=transport_or_cargo_keyboard())


async def cancel_handler(message: Message, state: FSMContext):
  current_state = await state.get_state()
  if current_state is None:
    return
  await state.clear()
  await message.answer("Bekor qilindi.", reply_markup=main_menu_keyboard())

async def admin_menu(message: types.Message):
  if message.from_user.id in ADMIN_IDS:
    from keyboards.admin import admin_keyboard
    await message.answer("Admin menu", reply_markup=admin_keyboard())