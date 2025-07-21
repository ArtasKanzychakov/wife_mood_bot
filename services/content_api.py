import aiohttp
import json
from config.settings import Config
from config.fallbacks import FALLBACK_CONTENT
import logging

async def get_giphy_gif(query: str) -> str:
    try:
        url = f"https://api.giphy.com/v1/gifs/random?api_key={Config.GIPHY_KEY}&tag={query}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['data']['images']['original']['url']
                return FALLBACK_CONTENT["gif_url"]
    except Exception as e:
        logging.error(f"Giphy API error: {e}")
        return FALLBACK_CONTENT["gif_url"]

async def get_unsplash_photo(query: str) -> str:
    try:
        url = f"https://api.unsplash.com/photos/random?query={query}&client_id={Config.UNSPLASH_KEY}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['urls']['regular']
                return FALLBACK_CONTENT["photo_url"]
    except Exception as e:
        logging.error(f"Unsplash API error: {e}")
        return FALLBACK_CONTENT["photo_url"]

async def get_yandex_music_tracks() -> list:
    try:
        url = "https://api.music.yandex.net/chart"
        headers = {"Authorization": f"OAuth {Config.YANDEX_MUSIC_KEY}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=Config.REQUEST_TIMEOUT) as response:
                if response.status == 200:
                    data = await response.json()
                    return [{
                        'title': track['title'],
                        'artist': track['artists'][0]['name'],
                        'link': track['link']
                    } for track in data['chart']['tracks'][:2]]
                return FALLBACK_CONTENT["music"]
    except Exception as e:
        logging.error(f"Yandex Music error: {e}")
        return FALLBACK_CONTENT["music"]
