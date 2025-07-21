# app/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.ext import Application
from datetime import datetime

from modules import (
    horoscopes, moon_cycles, jokes, psychology,
    esoterica, recipes, exercises, news,
    investment_news, investment_abc, audio_affirmations
)

# ID чата — будет получен динамически при старте
TARGET_CHAT_ID = None

def setup_scheduler(app: Application):
    scheduler = AsyncIOScheduler()

    # Расписание по времени (утро и вечер)
    scheduler.add_job(lambda: send_morning(app), 'cron', hour=8)
    scheduler.add_job(lambda: send_evening(app), 'cron', hour=20)

    # Почасовая активность
    scheduler.add_job(lambda: send_hourly_content(app), 'cron', minute=0)

    scheduler.start()

async def send_morning(app: Application):
    if not TARGET_CHAT_ID:
        return

    # Мудрость, луна, рецепт, аффирмация
    moon = await moon_cycles.get_today_moon_phase()
    affirmation = await audio_affirmations.get_affirmation()
    recipe = await recipes.get_recipe()
    greeting = f"""🌞 Доброе утро!

🧘 Практика дня: {await psychology.get_tip(short=True)}
🌙 {moon}
🍽 Блюдо дня: {recipe.splitlines()[0]}

🎧 Аффирмация в аудио:
"""
    await app.bot.send_message(chat_id=TARGET_CHAT_ID, text=greeting)
    await app.bot.send_audio(chat_id=TARGET_CHAT_ID, audio=affirmation)

async def send_evening(app: Application):
    if not TARGET_CHAT_ID:
        return

    msg = f"""🌙 Спокойного вечера!

🏃‍♀️ Упражнение ЛФК: {await exercises.get_evening_exercise()}
🎧 Аффирмация: {await audio_affirmations.get_evening_text()}
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
        await fashion.get_tip()
    ]

    # Распределяем циклично
    index = now % len(content_list)
    content = content_list[index]

    await app.bot.send_message(chat_id=TARGET_CHAT_ID, text=content)

# Используется из bot.py для установки chat_id
def set_target_chat(chat_id: int):
    global TARGET_CHAT_ID
    TARGET_CHAT_ID = chat_id
