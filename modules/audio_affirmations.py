# modules/audio_affirmations.py

import aiohttp
import urllib.parse

AFFIRMATIONS = [
    "Ты прекрасна и сильна.",
    "Каждый день приносит новые возможности.",
    "Любовь и счастье окружают тебя.",
    "Ты достойна всего самого лучшего."
]

TTS_API = "https://ttsmp3.com/makemp3_new.php"

async def get_affirmation():
    text = AFFIRMATIONS[0]  # Можно рандомизировать
    data = {
        "msg": text,
        "lang": "Joanna",
        "source": "ttsmp3"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(TTS_API, data=data) as resp:
            res = await resp.json()
            url = res.get("URL")
            return url  # URL аудиофайла
