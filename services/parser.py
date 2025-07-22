import aiohttp
from bs4 import BeautifulSoup
from config.settings import Config
from config.fallbacks import FALLBACK_CONTENT
import logging
from datetime import datetime

async def parse_business_news(session: aiohttp.ClientSession) -> list:
    """
    Получаем бизнес-новости через NewsAPI с fallback на парсинг Finam
    """
    try:
        # Пробуем NewsAPI (основной источник)
        news = await _fetch_newsapi(session)
        if news:
            return news
            
        # Если NewsAPI не сработал - парсим Finam
        return await _parse_finam_fallback(session)
        
    except Exception as e:
        logging.error(f"News parsing error: {e}")
        return FALLBACK_CONTENT["business_news"]

async def _fetch_newsapi(session: aiohttp.ClientSession) -> list:
    """Получение новостей через NewsAPI"""
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=ru&category=business&pageSize=5&apiKey={Config.NEWSAPI_KEY}"
        
        async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
            if response.status == 200:
                data = await response.json()
                return [{
                    'title': article['title'],
                    'url': article['url'],
                    'source': article['source']['name']
                } for article in data['articles']]
    except Exception as e:
        logging.warning(f"NewsAPI failed, using fallback: {str(e)}")
        return None

async def _parse_finam_fallback(session: aiohttp.ClientSession) -> list:
    """Fallback-парсинг Finam.ru"""
    try:
        url = "https://www.finam.ru/news/"
        
        async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                
                news_items = soup.select('.news-list__item')[:5]
                return [{
                    'title': item.find('a').get_text(strip=True),
                    'url': f"https://www.finam.ru{item.find('a')['href']}",
                    'source': 'Finam.ru'
                } for item in news_items]
                
        return FALLBACK_CONTENT["business_news"]
    except Exception as e:
        logging.error(f"Finam parsing failed: {str(e)}")
        return FALLBACK_CONTENT["business_news"]

async def parse_horoscope(session: aiohttp.ClientSession, zodiac: str) -> str:
    """Парсинг гороскопа (остаётся без изменений)"""
    try:
        url = f"https://horo.mail.ru/prediction/{zodiac}/today/"
        async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                prediction = soup.find('div', class_='article__item')
                return prediction.get_text(strip=True) if prediction else FALLBACK_CONTENT["horoscope"]
            return FALLBACK_CONTENT["horoscope"]
    except Exception as e:
        logging.error(f"Horo parse error: {e}")
        return FALLBACK_CONTENT["horoscope"]

async def parse_lunar_calendar(session: aiohttp.ClientSession) -> dict:
    """Парсинг лунного календаря (остаётся без изменений)"""
    try:
        url = "https://lunnyjkalendar.ru/"
        async with session.get(url, timeout=Config.REQUEST_TIMEOUT) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                day = soup.find('div', class_='moon-day').get_text(strip=True)
                advice = soup.find('div', class_='moon-advice').get_text(strip=True)
                return {'day': day, 'advice': advice}
            return {'day': '12-й', 'advice': 'Благоприятный день'}
    except Exception as e:
        logging.error(f"Lunar parse error: {e}")
        return {'day': '12-й', 'advice': 'Благоприятный день'}
