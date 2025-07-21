# modules/horoscopes.py

import aiohttp

# Знак зодиака вашей жены — укажите нужный!
ZODIAC_SIGN = "leo"  # пример: "aries", "taurus", "gemini", ..., "leo"

API_URL = "https://aztro.sameerkumar.website/?sign={sign}&day=today"

async def get_today_horoscope():
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL.format(sign=ZODIAC_SIGN)) as resp:
            data = await resp.json()
            return f"🔮 Гороскоп на сегодня для {ZODIAC_SIGN.title()}:\n\n{data['description']}"
