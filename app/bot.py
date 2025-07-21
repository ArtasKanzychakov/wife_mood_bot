# app/bot.py

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputMediaPhoto
from aiogram.utils import executor
from dotenv import load_dotenv
import os

from app.handlers import get_reaction_keyboard, reaction_callback_handler
from modules import fashion, recipes

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Глобальное хранилище для chat_id
TARGET_CHAT_ID = None

@dp.message_handler(commands=["start", "go"])
async def start_command(message: types.Message):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = message.chat.id
    await message.answer("Привет! Я твой бот-настроение 🌸")

@dp.message_handler(commands=["fashion"])
async def fashion_command(message: types.Message):
    media = await fashion.get_fashion_images()
    if media:
        await bot.send_media_group(chat_id=message.chat.id, media=[types.InputMediaPhoto(**m) for m in media])
        await message.answer("Это модные образы дня", reply_markup=get_reaction_keyboard())

@dp.message_handler(commands=["рецепт"])
async def recipe_command(message: types.Message):
    media = await recipes.get_recipe_carousel()
    if media:
        await bot.send_media_group(chat_id=message.chat.id, media=[types.InputMediaPhoto(**m) for m in media])
        await message.answer("Вот вкусные рецепты дня 🍽", reply_markup=get_reaction_keyboard())

@dp.callback_query_handler()
async def handle_callback(callback_query: types.CallbackQuery):
    await reaction_callback_handler(callback_query)

if __name__ == "__main__":
    from app.webhook import setup_webhook
    asyncio.run(setup_webhook(bot))
    executor.start_polling(dp, skip_updates=True)
