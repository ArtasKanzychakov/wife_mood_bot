# modules/fashion.py

import aiohttp
from bs4 import BeautifulSoup

async def get_fashion_images():
    url = "https://www.vogue.ru/fashion"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    articles = soup.find_all("article", limit=5)

    photos = []
    for article in articles:
        img = article.find("img")
        if img and img.get("src"):
            photos.append({
                "type": "photo",
                "media": img["src"],
                "caption": "🧥 Модные тренды от Vogue"
            })

    return photos
