from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Foydalanuvchilarni ko'rish", callback_data="admin_view_users")
    builder.button(text="Postlarni ko'rish", callback_data="admin_view_posts")
    builder.button(text="Barchaga xabar jo'natish", callback_data="admin_send_message")
    builder.adjust(1)
    return builder.as_markup()

def user_pagination_keyboard(user_id: int, current_index:int, total_users: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️", callback_data="admin_prev_user")
    builder.button(text=f"{current_index + 1}/{total_users}", callback_data="ignore")
    builder.button(text="➡️", callback_data="admin_next_user")
    builder.button(text="O'chirish 🗑️", callback_data=f"admin_delete_user:{user_id}")
    builder.adjust(3,1)
    return builder.as_markup()


def post_pagination_keyboard(user_id:str, post_id: str, current_index:int, total_posts: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️", callback_data="admin_prev_post")
    builder.button(text=f"{current_index + 1}/{total_posts}", callback_data="ignore")
    builder.button(text="➡️", callback_data="admin_next_post")
    builder.button(text="O'chirish", callback_data=f"admin_delete_post:{user_id}_{post_id}")
    builder.adjust(3,1)
    return builder.as_markup()