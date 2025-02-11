from aiogram.utils.keyboard import InlineKeyboardBuilder


def post_confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Tasdiqlash", callback_data=f"confirm_post:True")
    builder.button(text="Bekor qilish", callback_data=f"confirm_post:False")
    return builder.as_markup()
