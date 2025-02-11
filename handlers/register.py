from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.data_manager import DataManager
from keyboards.common import main_menu_keyboard


async def register_phone(message: types.Message, state: FSMContext):
    try:
        phone = message.contact.phone_number
        await state.update_data(phone_number=phone)
        await state.set_state("register:fullname")
        await message.answer("To'liq ismingizni kiriting:", reply_markup=types.ReplyKeyboardRemove())
    except AttributeError:
        await message.answer("Xato telefon raqam! iltimos pastdagi tugmani bosish orqali raqamingizni ulashing:")

async def register_fullname(message: types.Message, state: FSMContext):
    fullname = str(message.text)
    for letter in fullname:
        if letter.isdigit():
            await message.answer("Iltimos haqiqiy ismingizni kiriting:")
            return
    await state.update_data(fullname=fullname)

    user_data = await state.get_data()
    user_id = message.from_user.id

    user_data_to_save = {
         str(user_id): {
            "fullname": user_data["fullname"],
            "username": message.from_user.username,
            "phone_number": user_data["phone_number"]
        }
    }
    user_manager = DataManager("users.json")
    user_manager.create(user_data_to_save)
    user_manager = DataManager("posts.json")
    user_manager.create({str(user_id): {}})

    await state.clear()
    await message.answer("Siz Ro'yxatdan o'tdingiz \nIltimos kerakli amalni tanlang:", reply_markup=main_menu_keyboard())

