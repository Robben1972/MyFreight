from aiogram import types
from aiogram.fsm.context import FSMContext

from config import ADMIN_IDS
from keyboards.admin import admin_keyboard, user_pagination_keyboard, post_pagination_keyboard
from utils.data_manager import DataManager

async def admin_view_users(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("Siz admin emassiz")
        return

    user_manager = DataManager("users.json")
    users = user_manager.get_all()

    if not users:
        await call.answer("Foydalanuvchilar topilmadi")
        return
    
    await state.set_data({"users": list(users.keys()), "current_user_index": 0}) 
    await show_user(call, state)


async def show_user(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    users_ids = state_data.get("users")
    current_user_index = state_data.get("current_user_index")
    
    if not users_ids or not isinstance(current_user_index,int) or not 0 <= current_user_index < len(users_ids):
        await call.answer("Xatolik bo'ldi", show_alert=True)
        return

    user_manager = DataManager("users.json")
    user_id = users_ids[current_user_index]
    user_data = user_manager.get_by_id(user_id)

    if user_data:
      await call.message.edit_text(
            f"Foydalanuvchi: {user_data['fullname']}",
            reply_markup=user_pagination_keyboard(user_id, current_user_index,len(users_ids))
        )
    else:
        await call.answer("Foydalanuvchi topilmadi", show_alert=True)
        

async def admin_prev_user(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    current_user_index = state_data.get("current_user_index")
    if not isinstance(current_user_index, int):
         await call.answer("Xatolik bo'ldi", show_alert=True)
         return
    if current_user_index > 0:
        await state.update_data(current_user_index = current_user_index - 1)
        await show_user(call, state)
    else:
       await call.answer("Bu birinchi foydalanuvchi", show_alert=True)


async def admin_next_user(call: types.CallbackQuery, state: FSMContext):
   state_data = await state.get_data()
   users_ids = state_data.get("users")
   current_user_index = state_data.get("current_user_index")
   if not isinstance(current_user_index, int):
         await call.answer("Mavjud emas", show_alert=True)
         return
   if users_ids and current_user_index < len(users_ids) - 1:
        await state.update_data(current_user_index = current_user_index + 1)
        await show_user(call, state)
   else:
       await call.answer("Bu oxirgi foydalanuvchi", show_alert=True)


async def admin_view_posts(call: types.CallbackQuery, state: FSMContext):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("Siz admin emassiz")
        return

    post_manager = DataManager("posts.json")
    posts = post_manager.get_all()
    if not posts:
        await call.answer("Postlar topilmadi")
        return

    post_ids = []
    for user_id, user_posts in posts.items():
      for post_id in user_posts:
        post_ids.append((user_id,post_id))
    
    await state.set_data({"post_ids": post_ids, "current_post_index": 0})
    await show_post(call, state)


async def show_post(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    post_ids = state_data.get("post_ids")
    current_post_index = state_data.get("current_post_index")

    if not post_ids or not isinstance(current_post_index,int) or not 0 <= current_post_index < len(post_ids):
      await call.answer("Mavjud emas", show_alert=True)
      return

    post_manager = DataManager("posts.json")
    users_manager = DataManager("users.json")
    regions_manager = DataManager("regions.json")
    cities_manager = DataManager("cities.json").get_all()

    user_id,post_id = post_ids[current_post_index]
    post = post_manager.get_by_id(user_id).get(str(post_id))
    if post:
      user = users_manager.get_by_id(str(post['created_by']))
      from_region = regions_manager.get_by_id(post['region_id_from'])
      to_region = regions_manager.get_by_id(post['region_id_to'])
      
      from_region_name = from_region["region_name"] if from_region else "N/A"
      from_city_name = "N/A"
      for id in cities_manager:
          if cities_manager[id]["region_id"] == post['region_id_from'] and cities_manager[id]['id'] == post['city_id_from']:
               from_city_name = cities_manager[id]["city_name"]
               break
      to_region_name = to_region["region_name"] if to_region else "N/A"
      to_city_name = "N/A"
      for id in cities_manager:
          if cities_manager[id]["region_id"] == post['region_id_to'] and cities_manager[id]['id'] == post['city_id_to']:
               to_city_name = cities_manager[id]["city_name"]
               break

      text = f"""Name: {post['name']}
Treyler: {post['vehicle']}
Og'irligi: {post['weight']}
Yuklanadigan Viloyat: {from_region_name} - {from_city_name}
Olib boriladigan Viloyat: {to_region_name} - {to_city_name}
Izoh: {post['description']}
Narxi: {post['price']}
Status: {post['status']}
Yuklash vaqti: {post['delivery_datetime']}
Buyurtma: {post['order']}
Egasi: {user['fullname'] if user else "N/A"}
"""
      await call.message.edit_text(f"Post:\n {text}", reply_markup=post_pagination_keyboard(user_id, post_id,current_post_index, len(post_ids)))
    else:
      await call.answer("Post topilmadi", show_alert=True)


async def admin_prev_post(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    current_post_index = state_data.get("current_post_index")
    if not isinstance(current_post_index, int):
         await call.answer("Mavjud emas", show_alert=True)
         return
    if current_post_index > 0:
        await state.update_data(current_post_index = current_post_index - 1)
        await show_post(call, state)
    else:
       await call.answer("Bu birinchi post", show_alert=True)

async def admin_next_post(call: types.CallbackQuery, state: FSMContext):
   state_data = await state.get_data()
   post_ids = state_data.get("post_ids")
   current_post_index = state_data.get("current_post_index")
   if not isinstance(current_post_index, int):
         await call.answer("Mavjud emas", show_alert=True)
         return
   if post_ids and current_post_index < len(post_ids) - 1:
        await state.update_data(current_post_index = current_post_index + 1)
        await show_post(call, state)
   else:
       await call.answer("Bu oxirgi post", show_alert=True)


async def admin_delete_post(call: types.CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
        await call.answer("Siz admin emassiz")
        return

    post_id_parts = call.data.split(":")[1].split("_")
    user_id = post_id_parts[0]
    post_id = post_id_parts[1]

    post_manager = DataManager("posts.json")
    post_manager.delete_post(user_id, post_id)

    await call.message.answer(f"Post {post_id} o'chirildi", show_alert=True, reply_markup=admin_keyboard())
    await call.message.delete()


async def admin_delete_user(call: types.CallbackQuery):
    if call.from_user.id not in ADMIN_IDS:
       await call.answer("Siz admin emassiz")
       return
    user_id = call.data.split(':')[1]
    user_manager = DataManager("users.json")
    user = user_manager.delete(user_id)
    if user:
       await call.message.answer("Foydalanuvchi o'chirildi", reply_markup=admin_keyboard())
       await call.message.delete()
    else:
       await call.message.answer("Xatolik")


async def admin_send_message(call: types.CallbackQuery, state: FSMContext):
   if call.from_user.id not in ADMIN_IDS:
       await call.answer("Siz admin emassiz")
       return
   await state.set_state("admin:message")
   await call.message.answer("Barcha uchun xabarni yozing:", reply_markup=types.ReplyKeyboardRemove())

async def admin_send_message_to_all(message: types.Message, bot, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
       return
    users_manager = DataManager("users.json")
    users = users_manager.get_all()
    for user in users:
        try:
           await bot.send_message(int(user), message.text)
        except Exception:
            pass
    await state.clear()
    await message.answer("Xabar hammaga junatildi", reply_markup=admin_keyboard())