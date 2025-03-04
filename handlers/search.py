from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.common import back_keyboard, get_region_keyboard, get_type_of_trailer_keyboard
from keyboards.search import search_post_pagination_keyboard
from utils.data_manager import DataManager
from keyboards.common import main_menu_keyboard
from config import bot  #Import bot from config

messages_id = []

async def search_select_type(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    if message.text == "Yuk":
        await state.set_state("search:cargo_name")
        await message.answer("Yuk nomini kiriting:", reply_markup=back_keyboard())
    # elif message.text == "Transport":
    #     await state.set_state("search:trailer_type")
    #     await message.answer("Avtomobil turini tanlang:", reply_markup=get_type_of_trailer_keyboard())

async def search_trailer_type(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    await state.update_data(trailer_type=message.text)
    regions = DataManager("regions.json").get_all()
    await state.set_state("search:region_from")
    await message.answer("Yuklanadigan Viloyatni tanlang:", reply_markup=get_region_keyboard(regions))

async def search_cargo_name(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    await state.update_data(name=message.text)
    regions = DataManager("regions.json").get_all()
    await state.set_state("search:region_from_vehicle")  # Different state for vehicle
    await message.answer("Yuklanadigan Viloyatni tanlang:", reply_markup=get_region_keyboard(regions))

async def search_region_from(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_from=region_item["id"])
            regions = DataManager("regions.json").get_all()
            await state.set_state("search:region_to")
            await message.answer("Boriladigan Viloyatni tanlang:", reply_markup=get_region_keyboard(regions))
            return
    await message.answer("Iltimos to'g'ri viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def search_region_from_vehicle(message: types.Message, state: FSMContext):  # Different function
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_from=region_item["id"])
            regions = DataManager("regions.json").get_all()
            await state.set_state("search:region_to_vehicle")  # Different state
            await message.answer("Boriladigan Viloyatni tanlang:", reply_markup=get_region_keyboard(regions))
            return
    await message.answer("Iltimos to'g'ri viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def search_region_to(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_to=region_item["id"])
            data = await state.get_data()
            await clear_ids(message.from_user.id)
            await state.clear()
            await search_posts(message, state, data) # Pass state
            return
    await message.answer("Iltimos to'g'ri viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def search_region_to_vehicle(message: types.Message, state: FSMContext): # Different function
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_to=region_item["id"])
            data = await state.get_data()
            await clear_ids(message.from_user.id)
            await state.clear()
            await search_posts_vehicles(message, state, data) # Pass state
            return
    await message.answer("Iltimos to'g'ri viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def search_posts(message: types.Message, state: FSMContext, data): # Added state
    messages_id.append(message.message_id)
    post_manager = DataManager("posts.json")
    posts = post_manager.get_all()
    found_posts = []
    for user_id, user_posts in posts.items():  # Include user_id
        for post_id, post_data in user_posts.items():
            if (
                post_data['status'] == "active" and
                post_data['region_id_from'] == data['region_id_from'] and
                post_data['region_id_to'] == data['region_id_to'] and
                post_data['order'] == "cargo"
            ):
                found_posts.append((user_id, post_id, post_data))  # Store user_id and post_id

    if found_posts:
        await message.answer('Topilgan postlar', reply_markup=ReplyKeyboardRemove())
        await state.set_data({"found_posts": found_posts, "current_post_index": 0})
        await show_post(message, state)
    else:
        await message.answer("Post topilmadi", reply_markup=main_menu_keyboard())
        await clear_ids(message.from_user.id)

async def search_posts_vehicles(message: types.Message, state: FSMContext, data):  # Added state
    messages_id.append(message.message_id)
    post_manager = DataManager("posts.json")
    posts = post_manager.get_all()
    found_posts = []
    for user_id, user_posts in posts.items():  # Include user_id
        for post_id, post_data in user_posts.items():
            if (
                post_data['status'] == "active" and
                post_data['region_id_from'] == data['region_id_from'] and
                post_data['region_id_to'] == data['region_id_to'] and
                post_data['order'] == "cargo"
            ):
                found_posts.append((user_id, post_id, post_data))  # Store user_id and post_id
    if found_posts:
        await message.answer('Topilgan postlar', reply_markup=ReplyKeyboardRemove())
        await state.set_data({"found_posts": found_posts, "current_post_index": 0})
        await show_post(message, state)
    else:
        await message.answer("Post topilmadi", reply_markup=main_menu_keyboard())
        await clear_ids(message.from_user.id)

async def show_post(message: types.Message, state: FSMContext): # new function
    state_data = await state.get_data()
    found_posts = state_data.get("found_posts")
    current_post_index = state_data.get("current_post_index", 0)

    if not found_posts:
        await message.answer("Post topilmadi", reply_markup=main_menu_keyboard())
        return

    if not (0 <= current_post_index < len(found_posts)):
        await message.answer("Mavjud emas")
        return

    user_id, post_id, post = found_posts[current_post_index]
    post_text = ""
    if post['order'] == "transport":
      post_text = f"Transport: {post['vehicle']}\n Og'irligi: {post['weight']}\n Izoh: {post['description']}\n Narxi: {post['price']}"
    else:
      post_text = f"Yukning Nomi: {post['name']}\nYukning Vazni: {post['weight']}\nIzoh: {post['description']}\nNarxi: {post['price']}"
    await message.answer(
        post_text,
        reply_markup=search_post_pagination_keyboard(user_id, post_id, current_post_index, len(found_posts)) #New keyboard with pagination
    )

async def navigate_posts(call: types.CallbackQuery, state: FSMContext):
    action = call.data.split(":")[1]
    state_data = await state.get_data()
    found_posts = state_data.get("found_posts")
    current_post_index = state_data.get("current_post_index", 0)

    if action == "prev":
        current_post_index = max(0, current_post_index - 1)
    elif action == "next":
        current_post_index = min(len(found_posts) - 1, current_post_index + 1)

    await state.update_data(current_post_index=current_post_index)
    await call.message.delete()
    await show_post(call.message, state) # Pass message object

async def make_offer(call: types.CallbackQuery, state: FSMContext):
    post_id_parts = call.data.split(":")[1].split("_")
    print(post_id_parts)
    user_id = post_id_parts[0]
    post_id = post_id_parts[1]

    post_manager = DataManager("posts.json")
    users_manager = DataManager("users.json")
    post = post_manager.get_by_id(user_id).get(post_id)
    user = users_manager.get_by_id(user_id)

    if not post or not user:
        await call.answer("Post yoki user topilmadi", show_alert=True)
        return

    # Format user information
    user_info = f"Ismi 👤: {user['fullname']}\nTelefon raqami: {user['phone_number']}"

    # Inactive post status
    post['status'] = "inactive"
    post_manager.update_post(user_id, post_id, post)

    await call.message.edit_text(f"Shu insonga bog'lanishingiz mumkin\n\n{user_info}")
    await clear_ids(call.message.chat.id)
    await state.clear()
    await call.message.answer('Amalni tanlang', reply_markup=main_menu_keyboard())


async def clear_ids(chat_id: int):
    global messages_id
    for i in range(len(messages_id)):
        try:
            await bot.delete_message(chat_id, messages_id[i])
        except Exception as e:
            print(f"Error deleting message {messages_id[i]}: {e}")
    messages_id = []