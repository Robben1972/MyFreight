from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="E'lon berish")
    builder.button(text="Qidirish")
    return builder.as_markup(resize_keyboard=True)


def transport_or_cargo_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Yuk")
    builder.button(text="Transport")
    builder.row(KeyboardButton(text="Orqaga"))
    return builder.as_markup(resize_keyboard=True)


def back_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Orqaga")
    return builder.as_markup(resize_keyboard=True)

def get_region_keyboard(regions):
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=region['region_name']) for region in regions.values()]
    
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            builder.row(buttons[i], buttons[i+1])
        else:
            builder.row(buttons[i])

    builder.row(KeyboardButton(text="Orqaga"))
    return builder.as_markup(resize_keyboard=True)


def get_city_keyboard(cities):
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=city['city_name']) for city in cities.values()]

    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            builder.row(buttons[i], buttons[i+1])
        else:
            builder.row(buttons[i])

    builder.row(KeyboardButton(text="Orqaga"))
    return builder.as_markup(resize_keyboard=True)

def get_type_of_trailer_keyboard():
  builder = ReplyKeyboardBuilder()
  trailers = [
      'Sisterna' , 'Silos', 'Konteyner', 'Samosval', 'Mikro(10T)', 'Mikro(5T)', 'Mikro(2T)', 'Boshqa'
  ]
  for trailer in trailers:
    builder.button(text=trailer)
  builder.adjust(2)
  builder.row(KeyboardButton(text="Orqaga")) 
  return builder.as_markup(resize_keyboard=True)