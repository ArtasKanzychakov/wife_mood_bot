from aiohttp import ClientSession
from aiogram import Bot
from datetime import datetime, time
import asyncio
from pytz import timezone
from config.settings import Config
from . import parser, content_api
from handlers.schedule import send_daily_content
import logging

class Scheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.moscow_tz = timezone('Europe/Moscow')
        self.schedule = {
            time(7, 0): self.send_morning_exercises,
            time(9, 0): self.send_business_news,
            time(11, 0): self.send_music_tracks,
            # ... остальные временные точки
        }

    async def run(self):
        while True:
            now = datetime.now(self.moscow_tz).time()
            for scheduled_time, task in self.schedule.items():
                if scheduled_time.hour == now.hour and scheduled_time.minute == now.minute:
                    await task()
            await asyncio.sleep(60)

    async def send_morning_exercises(self):
        try:
            async with ClientSession() as session:
                gif_url = await content_api.get_giphy_gif("morning+exercise")
                await self.bot.send_animation(
                    chat_id=Config.CHAT_ID,
                    animation=gif_url,
                    caption="🧘 Утренняя зарядка! 3 упражнения на сегодня..."
                )
        except Exception as e:
            logging.error(f"Exercise error: {e}")

    async def send_business_news(self):
        try:
            async with ClientSession() as session:
                news = await parser.parse_business_news(session)
                text = "📈 Бизнес-новости:\n" + "\n".join(
                    f"{i+1}. {item['title']}" for i, item in enumerate(news[:3])
                )
                await self.bot.send_message(
                    chat_id=Config.CHAT_ID,
                    text=text
                )
        except Exception as e:
            logging.error(f"Business news error: {e}")

    async def send_music_tracks(self):
        try:
            tracks = await content_api.get_yandex_music_tracks()
            for track in tracks:
                await self.bot.send_audio(
                    chat_id=Config.CHAT_ID,
                    audio=track['link'],
                    caption=f"🎵 {track['artist']} - {track['title']}"
                )
        except Exception as e:
            logging.error(f"Music error: {e}")
