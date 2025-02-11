from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def search_post_pagination_keyboard(user_id: str, post_id: str, current_index: int, total_posts: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️", callback_data="navigate_posts:prev")
    builder.button(text=f"{current_index + 1}/{total_posts}", callback_data="ignore")
    builder.button(text="➡️", callback_data="navigate_posts:next")
    builder.button(text="Buyurtma berish", callback_data=f"make_offer:{user_id}_{post_id}")
    builder.adjust(3, 1)
    return builder.as_markup()