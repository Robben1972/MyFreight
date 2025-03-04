from aiogram import types
from aiogram.fsm.context import FSMContext
from datetime import datetime
import re
from utils.data_manager import DataManager
from config import bot
from keyboards.common import back_keyboard, get_region_keyboard, get_city_keyboard, get_type_of_trailer_keyboard, main_menu_keyboard
from keyboards.post import post_confirm_keyboard

messages_id = []


async def post_select_type(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    if message.text == "Yuk":
        await state.set_state("post:cargo_name")
        await message.answer("Yukning nomini yozing:", reply_markup=back_keyboard())

    # elif message.text == "Transport":
        # await state.set_state("post:trailer_type")
        # await message.answer("Treyler turini tanlang:", reply_markup=get_type_of_trailer_keyboard())




async def post_trailer_name(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    await state.update_data(name=message.text)
    await state.set_state("post:trailer_type")
    await message.answer("Treyler turini tanlang:", reply_markup=get_type_of_trailer_keyboard())

async def post_cargo_name(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    await state.update_data(name=message.text)
    await state.set_state("post:weight")
    await message.answer("Yukning vaznini kiriting (kg):", reply_markup=back_keyboard())



async def post_trailer_type(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    await state.update_data(trailer_type=message.text)
    await state.set_state("post:vehicle_weight")
    await message.answer("Yukning og'irligini kiriting (kg):", reply_markup=back_keyboard())


async def post_weight(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    try:
        weight = int(message.text)
        await state.update_data(weight=weight)
        regions = DataManager("regions.json").get_all()
        await state.set_state("post:region_from")
        await message.answer("Yuklash mintaqasini tanlang:", reply_markup=get_region_keyboard(regions))
    except ValueError:
        await message.answer('Iltimos faqat son kiriting')


async def post_vehicle_weight(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    try:
        weight = int(message.text)
        await state.update_data(weight=weight)
        regions = DataManager("regions.json").get_all()
        await state.set_state("post:vehicle_region_from")
        await message.answer("Yuklash mintaqasini tanlang:", reply_markup=get_region_keyboard(regions))
    except ValueError:
        await message.answer('Iltimos faqat son kiriting')

async def post_region_from(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_from=region_item["id"])
            cities = DataManager("cities.json").get_all()
            cities_by_region = {key: value for key, value in cities.items() if value["region_id"] == region_item["id"]}
            await state.set_state("post:city_from")
            await message.answer("Yuklash hududini tanlang:", reply_markup=get_city_keyboard(cities_by_region))
            return
    await message.answer("Iltimos mavjud viloyatni tanlang:", reply_markup=get_region_keyboard(region))


async def post_vehicle_region_from(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_from=region_item["id"])
            cities = DataManager("cities.json").get_all()
            cities_by_region = {key: value for key, value in cities.items() if value["region_id"] == region_item["id"]}
            await state.set_state("post:vehicle_city_from")
            await message.answer("Yuklash hududini tanlang:", reply_markup=get_city_keyboard(cities_by_region))
            return
    await message.answer("Iltimos mavjud viloyatni tanlang:", reply_markup=get_region_keyboard(region))


async def post_city_from(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    cities = DataManager("cities.json").get_all()
    for city in cities.values():
        if city["city_name"] == message.text:
            await state.update_data(city_id_from=city["id"])
            regions = DataManager("regions.json").get_all()
            await state.set_state("post:region_to")
            await message.answer("Yetkazib berish mintaqasini tanlang:", reply_markup=get_region_keyboard(regions))
            return
    cities_data = await state.get_data()
    cities = DataManager("cities.json").get_all()
    cities_by_region = {key: value for key, value in cities.items() if
                        value["region_id"] == cities_data["region_id_from"]}
    await message.answer("Iltimos mavjud bo'lgan shaharni tanlang", reply_markup=get_city_keyboard(cities_by_region))


async def post_vehicle_city_from(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    cities = DataManager("cities.json").get_all()
    for city in cities.values():
        if city["city_name"] == message.text:
            await state.update_data(city_id_from=city["id"])
            regions = DataManager("regions.json").get_all()
            await state.set_state("post:vehicle_region_to")
            await message.answer("Yetkazib berish mintaqasini tanlang:", reply_markup=get_region_keyboard(regions))
            return
    cities_data = await state.get_data()
    cities = DataManager("cities.json").get_all()
    cities_by_region = {key: value for key, value in cities.items() if
                        value["region_id"] == cities_data["region_id_from"]}
    await message.answer("Iltimos mavjud bo'lgan shaharni tanlang", reply_markup=get_city_keyboard(cities_by_region))

async def post_region_to(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_to=region_item["id"])
            cities = DataManager("cities.json").get_all()
            cities_by_region = {key: value for key, value in cities.items() if value["region_id"] == region_item["id"]}
            await state.set_state("post:city_to")
            await message.answer("Yetkazib berish hududini tanlang:", reply_markup=get_city_keyboard(cities_by_region))
            return
    await message.answer("Iltimos mavjud viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def post_vehicle_region_to(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    region = DataManager("regions.json").get_all()
    for region_item in region.values():
        if region_item["region_name"] == message.text:
            await state.update_data(region_id_to=region_item["id"])
            cities = DataManager("cities.json").get_all()
            cities_by_region = {key: value for key, value in cities.items() if value["region_id"] == region_item["id"]}
            await state.set_state("post:vehicle_city_to")
            await message.answer("Yetkazib berish hududini tanlang:", reply_markup=get_city_keyboard(cities_by_region))
            return
    await message.answer("Iltimos mavjud viloyatni tanlang:", reply_markup=get_region_keyboard(region))

async def post_city_to(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    cities = DataManager("cities.json").get_all()
    for city in cities.values():
        if city["city_name"] == message.text:
            await state.update_data(city_id_to=city["id"])
            await state.set_state("post:description")
            await message.answer("Qo'shimcha izoh qoldiring:", reply_markup=back_keyboard())
            return
    cities_data = await state.get_data()
    cities = DataManager("cities.json").get_all()
    cities_by_region = {key: value for key, value in cities.items() if
                        value["region_id"] == cities_data["region_id_to"]}
    await message.answer("Iltimos mavjud bo'lgan shaharni tanlang", reply_markup=get_city_keyboard(cities_by_region))

async def post_vehicle_city_to(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    cities = DataManager("cities.json").get_all()
    for city in cities.values():
        if city["city_name"] == message.text:
            await state.update_data(city_id_to=city["id"])
            await state.set_state("post:vehicle_description")
            await message.answer("Qo'shimcha izoh qoldiring:", reply_markup=back_keyboard())
            return
    cities_data = await state.get_data()
    cities = DataManager("cities.json").get_all()
    cities_by_region = {key: value for key, value in cities.items() if
                        value["region_id"] == cities_data["region_id_to"]}
    await message.answer("Iltimos mavjud bo'lgan shaharni tanlang", reply_markup=get_city_keyboard(cities_by_region))


async def post_description(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    await state.update_data(description=message.text)
    await state.set_state("post:price")
    await message.answer("Yetkazish narxini yozing (so'mda):", reply_markup=back_keyboard())


async def post_vehicle_description(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    await state.update_data(description=message.text)
    await state.set_state("post:vehicle_price")
    await message.answer("Yetkazish narxini yozing (so'mda):", reply_markup=back_keyboard())


async def post_price(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await state.set_state("post:delivery_datetime")
        await message.answer("Yuklash vaqtini yozing (Quyidagi formatda: 12.02.2025 09:00):", reply_markup=back_keyboard())
    except ValueError:
        await message.answer('Iltimos faqat son kiriting')


async def post_vehicle_price(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    try:
        price = int(message.text)
        await state.update_data(price=price)
        await state.set_state("post:delivery_datetime")
        await message.answer("Yuklash vaqtini yozing (Quyidagi formatda: 12.02.2025 09:00):", reply_markup=back_keyboard())
    except ValueError:
        await message.answer('Iltimos faqat son kiriting')


async def post_delivery_datetime(message: types.Message, state: FSMContext):
    messages_id.append(message.message_id)
    date_time_str = message.text
    try:
        delivery_datetime = datetime.strptime(date_time_str, '%d.%m.%Y %H:%M')
        await state.update_data(delivery_datetime=delivery_datetime.isoformat())
        data = await state.get_data()
        region_from = DataManager("regions.json").get_by_id(data["region_id_from"])
        city_from = DataManager("cities.json").get_all()
        for ids in city_from:
            if city_from[ids]["id"] == data["city_id_from"] and city_from[ids]["region_id"] == data["region_id_from"]:
                data["city_id_from"] = city_from[ids]["city_name"]
                break
        region_to = DataManager("regions.json").get_by_id(data["region_id_to"])
        city_to = DataManager("cities.json").get_all()
        for ids in city_to:
            if city_to[ids]["id"] == data["city_id_to"] and city_to[ids]["region_id"] == data["region_id_to"]:
                data["city_id_to"] = city_to[ids]["city_name"]
                break
        try:
            text = f"""\nYukning Nomi: {data["name"]}
Yukning Vazni: {data["weight"]} kg
Yukning Treyler turi: {data['trailer_type']}
Yuklash Hududi: {region_from['region_name']} - {data['city_id_from']}
Yetqazish Mazili: {region_to['region_name']} - {data['city_id_to']}
Izoh: {data["description"]}
Yetqazish Narxi: {data["price"]}
Yuklash Vaqti: {delivery_datetime.strftime('%d.%m.%Y %H:%M')}
    """
        except:
            text = f"""\nTransport: {data['trailer_type']}
Og'irligi: {data["weight"]} kg
Yuklanadigan Manzil: {region_from['region_name']} viloyati {data['city_id_from']} shahri
Boriladigan Mazil: {region_to['region_name']} viloyati {data['city_id_to']} shahri
Izoh: {data["description"]}
Narx: {data["price"]}
Yuklash Vaqti: {delivery_datetime.strftime('%d.%m.%Y %H:%M')}
    """
        await clear_ids(message.from_user.id)
        await message.answer(text, reply_markup=post_confirm_keyboard())
    except ValueError:
        await message.answer("Noto'g'ri format. Iltimos, kk.oyyyy soat:minut formatida kiriting (masalan: 12.02.2025 16:00):", reply_markup=back_keyboard())


async def confirm_post(call: types.CallbackQuery, state: FSMContext):
    post = call.data.split(":")[1]
    if post == 'True':
        data = await state.get_data()
        post_manager = DataManager("posts.json")
        try:
            name = data['name']
        except:
            name = 'None'
        try:
            vehicle = data["trailer_type"]
        except:
            vehicle = 'None'

        post_data = {
            "name": name,
            "vehicle": vehicle,
            "weight": data["weight"],
            "region_id_from": data["region_id_from"],
            "city_id_from": data["city_id_from"],
            "region_id_to": data["region_id_to"],
            "city_id_to": data["city_id_to"],
            "delivery_datetime": data["delivery_datetime"], 
            "description": data["description"],
            "price": data["price"],
            "status": "active",
            "created_by": call.from_user.id,
            "order": 'cargo' if name != 'None' else 'transport'
        }
        post_manager.create_post(call.from_user.id, post_data)
        await call.message.edit_text(f"E'lon yuklandi", reply_markup=None)
        await call.message.answer('Kerakli amalni tanlang', reply_markup=main_menu_keyboard())
        await state.clear()
    else:
        await call.message.edit_text("E'lon bekor qilindi", reply_markup=None)
        await call.message.answer('Kerakli amalni tanlang', reply_markup=main_menu_keyboard())
        await state.clear()


async def clear_ids(chat_id: int):
    global messages_id
    for i in range(len(messages_id)):
        if i != len(messages_id) - 1:
            await bot.delete_message(chat_id, messages_id[i])
            await bot.delete_message(chat_id, messages_id[i] + 1)
        else:
            await bot.delete_message(chat_id, messages_id[i])
    messages_id = []