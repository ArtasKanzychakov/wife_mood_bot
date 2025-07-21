# modules/moon_cycles.py

import datetime
import aiohttp

API_URL = "https://www.icalendar37.net/lunar/api/"

# Получаем фазу Луны по текущей дате
async def get_today_moon_phase():
    today = datetime.date.today()
    url = f"{API_URL}?lang=en&month={today.month}&year={today.year}&size=100&lightColor=white&shadeColor=black&texturize=true"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            day_data = data["month"][str(today.day)]
            phase = day_data["phaseName"]
            return f"Фаза Луны сегодня 🌕: {phase}"
