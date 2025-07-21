# app/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application
from datetime import datetime
from telegram import InputMediaPhoto, InlineKeyboardMarkup, InlineKeyboardButton

from modules import (
    horoscopes, moon_cycles, jokes, psychology,
    esoterica, recipes, exercises, news,
    investment_news, investment_abc, audio_affirmations,
    fashion  # добавлен модуль моды для карусели
)

# ID чата будет установлен из bot.py
TARGET_CHAT_ID = None

def setup_scheduler(app: Application):
    scheduler = AsyncIOScheduler()

    # Утреннее вдохновение
    scheduler.add_job(lambda: send_morning(app), 'cron', hour=8)
    
    # Вечерняя практика
    scheduler.add_job(lambda: send_evening(app), 'cron', hour=20)

    # Почасовой пинг
    scheduler.add_job(lambda: send_hourly_content(app), 'cron', minute=0)

    scheduler.start()

def set_target_chat(chat_id: int):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = chat_id

# Кнопки реакций
def get_reaction_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("❤️ Нравится", callback_data="like"),
            InlineKeyboardButton("👎 Не нравится", callback_data="dislike")
        ],
        [
            InlineKeyboardButton("🔁 Ещё", callback_data="refresh"),
            InlineKeyboardButton("↩️ Назад", callback_data="back")
        ]
    ])

async def send_morning(app: Application):
    if not TARGET_CHAT_ID:
        return

    moon = await moon_cycles.get_today_moon_phase()
    affirmation_audio = await audio_affirmations.get_affirmation()
    recipe = await recipes.get_recipe()
    inspiration = await psychology.get_tip(short=True)

    greeting = f"""🌞 Доброе утро!

🧘 Практика дня: {inspiration}
🌙 {moon}
🍽 Блюдо дня: {recipe.splitlines()[0]}

🎧 Аффирмация:
"""

    await app.bot.send_message(chat_id=TARGET_CHAT_ID, text=greeting)
    await app.bot.send_audio(chat_id=TARGET_CHAT_ID, audio=affirmation_audio)

    # Карусель модных фото как визуальное вдохновение
    media = await fashion.get_fashion_images()
    if media:
        media_group = [InputMediaPhoto(m["media"], caption=m.get("caption", "")) for m in media]
        await app.bot.send_media_group(chat_id=TARGET_CHAT_ID, media=media_group)
        await app.bot.send_message(chat_id=TARGET_CHAT_ID, text="Как тебе модные образы?", reply_markup=get_reaction_keyboard())

async def send_evening(app: Application):
    if not TARGET_CHAT_ID:
        return

    lfk = await exercises.get_evening_exercise()
    affirm_text = await audio_affirmations.get_evening_text()

    msg = f"""🌙 Спокойного вечера!

🏃‍♀️ Упражнение ЛФК: {lfk}
🎧 Аффирмация: {affirm_text}
"""

    await app.bot.send_message(chat_id=TARGET_CHAT_ID, text=msg)

async def send_hourly_content(app: Application):
    if not TARGET_CHAT_ID:
        return

    now = datetime.now().hour

    content_list = [
        await horoscopes.get_today_horoscope(),
        await jokes.get_joke(),
        await news.get_news(),
        await esoterica.get_tip(),
        await investment_news.get_news(),
        await investment_abc.get_tip(),
        await psychology.get_tip(short=True),
    ]

    index = now % len(content_list)
    content = content_list[index]

    await app.bot.send_message(chat_id=TARGET_CHAT_ID, text=content, reply_markup=get_reaction_keyboard())
