# modules/jokes.py

import aiohttp

URL = "https://official-joke-api.appspot.com/random_joke"

async def get_joke():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as resp:
            data = await resp.json()
            return f"😂 Анекдот дня:\n\n{data['setup']}\n{data['punchline']}"
