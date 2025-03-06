from aiogram import types
from aiogram.fsm.context import FSMContext
from utils.data_manager import DataManager
from keyboards.my_posts import my_posts_keyboard
from keyboards.common import main_menu_keyboard

async def show_my_posts(message: types.Message, state: FSMContext):
    user_id = str(message.from_user.id)
    post_manager = DataManager("posts.json")
    
    user_posts = post_manager.get_by_id(user_id)
    
    if not user_posts:
        await message.answer("Sizda hali e'lonlar yo'q")
        return
    
    posts_list = [(user_id, post_id, post_data) for post_id, post_data in user_posts.items()]
    await state.update_data(my_posts=posts_list, current_post_index=0)
    await display_post(message, state)

async def display_post(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    posts_list = state_data.get("my_posts")
    current_index = state_data.get("current_post_index", 0)
    
    if not posts_list or current_index >= len(posts_list):
        await message.answer("E'lonlar topilmadi")
        return
    
    user_id, post_id, post = posts_list[current_index]
    
    region_manager = DataManager("regions.json")
    city_manager = DataManager("cities.json")
    
    region_from = region_manager.get_by_id(post["region_id_from"])
    cities = city_manager.get_all()
    
    city_from_name = ""
    city_to_name = ""
    
    for city_id, city_data in cities.items():
        if city_data["id"] == post["city_id_from"] and city_data["region_id"] == post["region_id_from"]:
            city_from_name = city_data["city_name"]
        if city_data["id"] == post["city_id_to"] and city_data["region_id"] == post["region_id_to"]:
            city_to_name = city_data["city_name"]
    
    region_to = region_manager.get_by_id(post["region_id_to"])
    
    post_text = (
        f"Yukning Nomi: {post['name']}\n"
        f"Yukning Vazni: {post['weight']}\n"
        f"Izoh: {post['description']}\n"
        f"Narxi: {post['price']}\n"
        f"Treyler turi: {post['vehicle']}\n"
        f"Yuklash Hududi: {region_from['region_name']} - {city_from_name}\n"
        f"Yetkazish Manzili: {region_to['region_name']} - {city_to_name}\n"
        f"Yuklash Vaqti: {post['delivery_datetime']}\n"
        f"Status: {post['status']}"
    )
    
    is_active = post["status"] == "active"
    
    await message.answer(
        post_text,
        reply_markup=my_posts_keyboard(user_id, post_id, current_index, len(posts_list), is_active)
    )

async def navigate_my_posts(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split(":")[1]
    state_data = await state.get_data()
    posts_list = state_data.get("my_posts")
    current_index = state_data.get("current_post_index", 0)
    
    # Delete the current message first
    await callback.message.delete()
    
    if action == "prev":
        current_index = max(0, current_index - 1)
        await state.update_data(current_post_index=current_index)
        await display_post(callback.message, state)
        
    elif action == "next":
        current_index = min(len(posts_list) - 1, current_index + 1)
        await state.update_data(current_post_index=current_index)
        await display_post(callback.message, state)
        
    elif action == "back":
        await callback.message.answer("Asosiy menu", reply_markup=main_menu_keyboard())
        await state.clear()
        
    elif action == "deactivate":
        user_id, post_id = callback.data.split(":")[2].split("_")
        post_manager = DataManager("posts.json")
        post = post_manager.get_by_id(user_id)[post_id]
        post["status"] = "inactive"
        post_manager.update_post(user_id, post_id, post)
        await callback.answer("E'lon o'chirildi", show_alert=True)
        posts_list[current_index] = (user_id, post_id, post)
        await state.update_data(my_posts=posts_list, current_post_index=current_index)
        await display_post(callback.message, state)
        
    elif action == "activate":
        user_id, post_id = callback.data.split(":")[2].split("_")
        post_manager = DataManager("posts.json")
        post = post_manager.get_by_id(user_id)[post_id]
        post["status"] = "active"
        post_manager.update_post(user_id, post_id, post)
        await callback.answer("E'lon qo'shildi", show_alert=True)
        posts_list[current_index] = (user_id, post_id, post)
        await state.update_data(my_posts=posts_list, current_post_index=current_index)
        await display_post(callback.message, state)