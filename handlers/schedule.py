from aiogram import types, Bot
from aiohttp import ClientSession
from config.settings import Config
from config.fallbacks import FALLBACK_CONTENT
import logging
from datetime import datetime

async def send_daily_content(bot: Bot):
    try:
        async with ClientSession() as session:
            # Получаем гороскоп
            horoscope = await get_horoscope(session)
            
            # Формируем сообщение
            msg = format_daily_message(horoscope)
            
            # Отправляем всем пользователям
            users = get_all_users()  # Функция для получения всех пользователей из БД
            for user in users:
                try:
                    await bot.send_message(user.telegram_id, msg)
                except Exception as e:
                    logging.error(f"Error sending to user {user.telegram_id}: {e}")
    except Exception as e:
        logging.error(f"Daily content error: {e}")
        await send_fallback_content(bot)

async def get_horoscope(session):
    try:
        async with session.get(
            "https://horo.mail.ru/prediction/bli/",
            timeout=Config.REQUEST_TIMEOUT
        ) as resp:
            if resp.status == 200:
                return await parse_horoscope(await resp.text())
            return FALLBACK_CONTENT["horoscope"]
    except:
        return FALLBACK_CONTENT["horoscope"]

def format_daily_message(horoscope):
    current_date = datetime.now().strftime("%d.%m.%Y")
    return f"""
📅 {current_date}
{horoscope}

🌖 Лунный день: 12-й (Благоприятный для планирования)
☸️ Буддийский день: Медитация
"""

async def send_fallback_content(bot: Bot):
    users = get_all_users()
    for user in users:
        try:
            await bot.send_message(
                user.telegram_id,
                FALLBACK_CONTENT["horoscope"]
            )
        except:
            continue

def register_handlers(dp: Dispatcher):
    pass  # Для рассылки используются внешние триггеры
