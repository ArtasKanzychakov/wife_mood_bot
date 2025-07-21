# modules/investment_news.py

import aiohttp

API_URL = "https://newsapi.org/v2/top-headlines"
API_KEY = "ВАШ_NEWSAPI_КЛЮЧ"

async def get_news():
    params = {
        "category": "business",
        "language": "ru",
        "apiKey": API_KEY,
        "pageSize": 1
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL, params=params) as resp:
            data = await resp.json()
            if data.get("articles"):
                article = data["articles"][0]
                title = article["title"]
                url = article["url"]
                return f"💼 Инвестиционные новости:\n{title}\n{url}"
            else:
                return "Нет свежих новостей по инвестициям."
