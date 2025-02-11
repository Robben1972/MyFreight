import logging
import asyncio

from aiogram import Dispatcher
from aiogram.filters import Command, CommandStart, StateFilter
from config import bot
from handlers import common, register, post, search, admin

logging.basicConfig(level=logging.INFO)


dp = Dispatcher() 


def check_string(text: str):
    return lambda message: message.text == text

def starts_with(prefix: str):
    return lambda message: message.text.startswith(prefix)


# Register handlers
dp.message.register(common.start, CommandStart())
dp.message.register(common.back, lambda message: message.text == "Orqaga")
dp.message.register(common.select_transport_or_cargo, lambda message: message.text in ["E'lon berish", "Qidirish"])
dp.message.register(common.cancel_handler, Command("cancel"))
dp.message.register(common.admin_menu, Command("admin"))

# Register handlers
dp.message.register(register.register_phone, StateFilter("register:phone"))
dp.message.register(register.register_fullname, StateFilter("register:fullname"))

#post handlers
dp.message.register(post.post_select_type, StateFilter("post:select_type"))
dp.message.register(post.post_cargo_name, StateFilter("post:cargo_name"))
dp.message.register(post.post_trailer_type, StateFilter("post:trailer_type"))
dp.message.register(post.post_weight, StateFilter("post:weight"))
dp.message.register(post.post_vehicle_weight, StateFilter("post:vehicle_weight"))
dp.message.register(post.post_region_from, StateFilter("post:region_from"))
dp.message.register(post.post_region_to, StateFilter("post:region_to"))
dp.message.register(post.post_vehicle_region_from, StateFilter("post:vehicle_region_from"))
dp.message.register(post.post_vehicle_region_to, StateFilter("post:vehicle_region_to"))
dp.message.register(post.post_city_from, StateFilter("post:city_from"))
dp.message.register(post.post_city_to, StateFilter("post:city_to"))
dp.message.register(post.post_vehicle_city_from, StateFilter("post:vehicle_city_from"))
dp.message.register(post.post_vehicle_city_to, StateFilter("post:vehicle_city_to"))
dp.message.register(post.post_description, StateFilter("post:description"))
dp.message.register(post.post_vehicle_description, StateFilter("post:vehicle_description"))
dp.message.register(post.post_price, StateFilter("post:price"))
dp.message.register(post.post_vehicle_price, StateFilter("post:vehicle_price"))
dp.message.register(post.post_delivery_datetime, StateFilter("post:delivery_datetime"))



#search handlers
dp.message.register(search.search_select_type, StateFilter("search:select_type"))
dp.message.register(search.search_trailer_type, StateFilter("search:trailer_type"))
dp.message.register(search.search_cargo_name, StateFilter("search:cargo_name"))
dp.message.register(search.search_region_from, StateFilter("search:region_from"))
dp.message.register(search.search_region_to, StateFilter("search:region_to"))
dp.message.register(search.search_region_from_vehicle, StateFilter("search:region_from_vehicle"))
dp.message.register(search.search_region_to_vehicle, StateFilter("search:region_to_vehicle"))
dp.callback_query.register(search.navigate_posts, lambda callback: callback.data.startswith("navigate_posts:"))
dp.callback_query.register(search.make_offer, lambda callback: callback.data.startswith("make_offer:"))


#admin handlers
dp.callback_query.register(admin.admin_view_users, lambda callback: callback.data == "admin_view_users")
dp.callback_query.register(admin.admin_prev_user, lambda callback: callback.data == "admin_prev_user")
dp.callback_query.register(admin.admin_next_user, lambda callback: callback.data  == "admin_next_user")
dp.callback_query.register(admin.admin_view_posts, lambda callback: callback.data == "admin_view_posts")
dp.callback_query.register(admin.admin_prev_post, lambda callback: callback.data == "admin_prev_post")
dp.callback_query.register(admin.admin_next_post, lambda callback: callback.data == "admin_next_post")
dp.callback_query.register(admin.admin_delete_user, lambda callback: callback.data.startswith("admin_delete_user"))
dp.callback_query.register(admin.admin_delete_post, lambda callback: callback.data.startswith("admin_delete_post"))
dp.callback_query.register(admin.admin_send_message, lambda callback: callback.data == "admin_send_message")
dp.message.register(admin.admin_send_message_to_all, StateFilter("admin:message"))

#callback handlers
dp.callback_query.register(post.confirm_post, lambda callback: callback.data.startswith("confirm_post"))


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())