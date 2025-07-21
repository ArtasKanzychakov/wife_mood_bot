import aiohttp
from bs4 import BeautifulSoup
from config.settings import Config
from config.fallbacks import FALLBACK_CONTENT
import logging
from datetime import datetime

async def parse_horoscope(session: aiohttp.ClientSession, zodiac: str) -> str:
    try:
        url = f"https://horo.mail.ru/prediction/{zodiac}/today/"
        async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                prediction = soup.find('div', class_='article__item')
                return prediction.text.strip() if prediction else FALLBACK_CONTENT["horoscope"]
            return FALLBACK_CONTENT["horoscope"]
    except Exception as e:
        logging.error(f"Horo parse error: {e}")
        return FALLBACK_CONTENT["horoscope"]

async def parse_business_news(session: aiohttp.ClientSession) -> list:
    try:
        url = "https://www.rbc.ru/"
        async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                news_items = soup.select('.news-feed__item')[:5]
                return [{
                    'title': item.find('span', class_='news-feed__item__title').text.strip(),
                    'link': item['href']
                } for item in news_items]
            return FALLBACK_CONTENT["business_news"]
    except Exception as e:
        logging.error(f"News parse error: {e}")
        return FALLBACK_CONTENT["business_news"]

async def parse_lunar_calendar(session: aiohttp.ClientSession) -> dict:
    try:
        url = "https://lunnyjkalendar.ru/"
        async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                day = soup.find('div', class_='moon-day').text.strip()
                advice = soup.find('div', class_='moon-advice').text.strip()
                return {'day': day, 'advice': advice}
            return {'day': '12-й', 'advice': 'Благоприятный день'}
    except Exception as e:
        logging.error(f"Lunar parse error: {e}")
        return {'day': '12-й', 'advice': 'Благоприятный день'}
