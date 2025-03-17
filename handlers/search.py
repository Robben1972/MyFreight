from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboards.common import back_keyboard, get_region_keyboard, get_type_of_trailer_keyboard
from keyboards.search import search_post_pagination_keyboard
from utils.data_manager import DataManager
from keyboards.common import main_menu_keyboard
from config import bot

messages_id = []

async def search_select_type(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    if message.text == "Yuk":
        await state.set_state("search:cargo_name")
        await message.answer("Yuk nomini kiriting:", reply_markup=back_keyboard())
    elif message.text == "Transport":
        await state.set_state("search:trailer_type")
        await message.answer("Avtomobil turini tanlang:", reply_markup=get_type_of_trailer_keyboard())

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
    await state.set_state("search:region_from_vehicle")
    await message.answer("Yuklanadigan Viloyatni tanlang:", reply_markup=get_region_keyboard(regions))

async def search_region_from(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_from=region_item["id"])
            await state.set_state("search:trailer_type_after_region")
            await message.answer("Treyler turini tanlang:", reply_markup=get_type_of_trailer_keyboard())
            return
    await message.answer("Iltimos to'g'ri viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def search_region_from_vehicle(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_from=region_item["id"])
            await state.set_state("search:trailer_type_after_region_vehicle")
            await message.answer("Treyler turini tanlang:", reply_markup=get_type_of_trailer_keyboard())
            return
    await message.answer("Iltimos to'g'ri viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def search_trailer_type_after_region(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    await state.update_data(trailer_type=message.text)
    data = await state.get_data()
    await clear_ids(message.chat.id, starting_message_id=min(messages_id) if messages_id else None)
    await state.clear()
    await search_posts(message, state, data)

async def search_trailer_type_after_region_vehicle(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    await state.update_data(trailer_type=message.text)
    data = await state.get_data()
    await clear_ids(message.chat.id, starting_message_id=min(messages_id) if messages_id else None)
    await state.clear()
    await search_posts_vehicles(message, state, data)

async def search_region_to(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_to=region_item["id"])
            data = await state.get_data()
            await clear_ids(message.chat.id, starting_message_id=min(messages_id) if messages_id else None)
            await state.clear()
            await search_posts(message, state, data)
            return
    await message.answer("Iltimos to'g'ri viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def search_region_to_vehicle(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_to=region_item["id"])
            data = await state.get_data()
            await clear_ids(message.chat.id, starting_message_id=min(messages_id) if messages_id else None)
            await state.clear()
            await search_posts_vehicles(message, state, data)
            return
    await message.answer("Iltimos to'g'ri viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def search_posts(message: types.Message, state: FSMContext, data):
    post_manager = DataManager("posts.json")
    posts = post_manager.get_all()
    found_posts = []
    for user_id, user_posts in posts.items():
        for post_id, post_data in user_posts.items():
            if (
                post_data['status'] == "active" and
                post_data['region_id_from'] == data['region_id_from'] and
                post_data.get('vehicle') == data.get('trailer_type')
            ):
                found_posts.append((user_id, post_id, post_data))

    if found_posts:
        await message.answer('Topilgan postlar', reply_markup=ReplyKeyboardRemove())
        await state.set_data({"found_posts": found_posts, "current_post_index": 0})
        await show_post(message, state)
    else:
        await message.answer("Post topilmadi", reply_markup=main_menu_keyboard())

async def search_posts_vehicles(message: types.Message, state: FSMContext, data):
    post_manager = DataManager("posts.json")
    posts = post_manager.get_all()
    found_posts = []
    for user_id, user_posts in posts.items():
        for post_id, post_data in user_posts.items():
            if (
                post_data['status'] == "active" and
                post_data['region_id_from'] == data['region_id_from'] and
                post_data.get('vehicle') == data.get('trailer_type')
            ):
                found_posts.append((user_id, post_id, post_data))
    if found_posts:
        await message.answer('Topilgan postlar', reply_markup=ReplyKeyboardRemove())
        await state.set_data({"found_posts": found_posts, "current_post_index": 0})
        await show_post(message, state)
    else:
        await message.answer("Post topilmadi", reply_markup=main_menu_keyboard())



async def show_post(message: types.Message, state: FSMContext):
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
    data = {}
    region_from = DataManager("regions.json").get_by_id(post["region_id_from"])
    city_from = DataManager("cities.json").get_all()
    for ids in city_from:
                if city_from[ids]["id"] == post["city_id_from"] and city_from[ids]["region_id"] == post["region_id_from"]:
                    data["city_id_from"] = city_from[ids]["city_name"]
                    break
    region_to = DataManager("regions.json").get_by_id(post["region_id_to"])
    city_to = DataManager("cities.json").get_all()
    for ids in city_to:
                if city_to[ids]["id"] == post["city_id_to"] and city_to[ids]["region_id"] == post["region_id_to"]:
                    data["city_id_to"] = city_to[ids]["city_name"]
                    break
    post_text = ""
    if post['order'] == "transport":
        post_text = f"Transport: {post['vehicle']}\nOg'irligi: {post['weight']}\nIzoh: {post['description']}\nNarxi: {post['price']}"
    else:
        post_text = f"Yukning Nomi: {post['name']}\nYukning Vazni: {post['weight']}\nIzoh: {post['description']}\nNarxi: {post['price']}\nYukning Treyler turi: {post['vehicle']}\nYuklash Hududi: {region_from['region_name']} - {data['city_id_from']}\nYetkazish Mazili: {region_to['region_name']} - {data['city_id_to']}\nYuklash Vaqti: {post['delivery_datetime'].split('T')[0]} {post['delivery_datetime'].split('T')[1]}"
    await message.answer(
        post_text,
        reply_markup=search_post_pagination_keyboard(user_id, post_id, current_post_index, len(found_posts))
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
    await show_post(call.message, state)

async def make_offer(call: types.CallbackQuery, state: FSMContext):
    post_id_parts = call.data.split(":")[1].split("_")
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
    user_info = f"Ismi: {user['fullname']}\nTelefon raqami: {user['phone_number'] if '+' in user['phone_number'] else '+'+user['phone_number']} "

    await call.message.edit_text(f"Shu insonga bog'lanishingiz mumkin\n\n{user_info}")
    await clear_ids(call.message.chat.id)
    await state.clear()
    await call.message.answer('Amalni tanlang', reply_markup=main_menu_keyboard())

async def clear_ids(chat_id: int, starting_message_id: int = None):
    global messages_id
    try:
        if starting_message_id:
            current_message_id = starting_message_id
            while True:
                try:
                    await bot.delete_message(chat_id, current_message_id)
                    current_message_id += 1
                except Exception:
                    break
        else:
            for msg_id in messages_id:
                try:
                    await bot.delete_message(chat_id, msg_id)
                except Exception:
                    pass  
            messages_id = []
    except Exception as e:
        print(f"Error clearing messages: {e}")
    finally:
        messages_id = [] 