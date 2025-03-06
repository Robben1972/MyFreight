from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def my_posts_keyboard(user_id: str, post_id: str, current_index: int, total_posts: int, is_active: bool) -> InlineKeyboardMarkup:
    buttons = []
    
    # Previous button if not at first post
    if current_index > 0:
        buttons.append(
            InlineKeyboardButton(text="⬅️ Oldingi", callback_data=f"my_posts:prev:{user_id}")
        )
    
    # Next button if not at last post
    if current_index < total_posts - 1:
        buttons.append(
            InlineKeyboardButton(text="Keyingi ➡️", callback_data=f"my_posts:next:{user_id}")
        )
    
    # Always show Back button
    buttons.append(
        InlineKeyboardButton(text="Orqaga", callback_data="my_posts:back")
    )
    
    # Show appropriate button based on post status
    if is_active:
        buttons.append(
            InlineKeyboardButton(text="O'chirish", callback_data=f"my_posts:deactivate:{user_id}_{post_id}")
        )
    else:
        buttons.append(
            InlineKeyboardButton(text="Qo'shish", callback_data=f"my_posts:activate:{user_id}_{post_id}")
        )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[buttons])
    return keyboard