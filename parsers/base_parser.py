import aiohttp
import asyncio
from bs4 import BeautifulSoup
from config.settings import Config
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class BaseParser:
    """Базовый класс для всех парсеров"""
    
    def __init__(self):
        self.cache = {}
        self.session = None
    
    async def get_session(self):
        """Получить сессию aiohttp"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=Config.REQUEST_TIMEOUT)
            )
        return self.session
    
    async def close(self):
        """Закрыть сессию"""
        if self.session:
            await self.session.close()
            self.session = None
    
    def get_cached(self, key):
        """Получить данные из кэша"""
        if key in self.cache:
            data, timestamp = self.cache[key]
            if datetime.now() - timestamp < timedelta(seconds=Config.CACHE_TIME):
                return data
        return None
    
    def set_cache(self, key, data):
        """Сохранить в кэш"""
        self.cache[key] = (data, datetime.now())
    
    async def fetch_html(self, url, headers=None):
        """Загрузить HTML страницу"""
        try:
            session = await self.get_session()
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    return await response.text()
                logger.error(f"HTTP {response.status} for {url}")
                return None
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    async def parse(self, *args, **kwargs):
        """Основной метод парсинга (переопределяется)"""
        raise NotImplementedError