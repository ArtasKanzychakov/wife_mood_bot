# app/handlers.py

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Клавиатура с реакциями
def get_reaction_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("❤️ Нравится", callback_data="like"),
        InlineKeyboardButton("👎 Не нравится", callback_data="dislike"),
        InlineKeyboardButton("🔁 Ещё", callback_data="refresh"),
        InlineKeyboardButton("↩️ Назад", callback_data="back")
    )

# Обработчик реакций
async def reaction_callback_handler(callback_query: types.CallbackQuery):
    action = callback_query.data
    if action == "like":
        await callback_query.answer("Рада, что тебе понравилось! 💖")
    elif action == "dislike":
        await callback_query.answer("Учту! 💬")
    elif action == "refresh":
        await callback_query.answer("Обновляю… 🔄")
        # Обновление можно подгрузить по контексту
    elif action == "back":
        await callback_query.answer("Возвращаемся назад… ⬅️")
