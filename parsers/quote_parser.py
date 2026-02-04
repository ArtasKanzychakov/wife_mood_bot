from .base_parser import BaseParser
from bs4 import BeautifulSoup
import logging
import random

logger = logging.getLogger(__name__)


class QuoteParser(BaseParser):
    """Парсер цитат"""
    
    async def parse(self):
        """Получить цитату дня"""
        cache_key = "quote_of_day"
        cached = self.get_cached(cache_key)
        if cached:
            return cached
        
        sources = [
            self._parse_citaty_info,
            self._get_fallback_quote
        ]
        
        for source in sources:
            try:
                quote = await source()
                if quote and len(quote) > 50:
                    self.set_cache(cache_key, quote)
                    return quote
            except Exception as e:
                logger.error(f"Quote source error: {e}")
                continue
        
        fallback = self._get_fallback_quote()
        self.set_cache(cache_key, fallback)
        return fallback
    
    async def _parse_citaty_info(self):
        """Парсить с citaty.info"""
        url = "https://citaty.info/random"
        html = await self.fetch_html(url)
        
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        quote_elem = soup.select_one('.field-type-text-with-summary')
        author_elem = soup.select_one('.field-type-text-with-summary + .field-items .field-item')
        
        if quote_elem and author_elem:
            quote = quote_elem.get_text(strip=True)
            author = author_elem.get_text(strip=True)
            return f"«{quote}»\n\n— {author}"
        
        return None
    
    def _get_fallback_quote(self):
        """Fallback цитаты"""
        quotes = [
            "«Лучший способ начать делать — перестать говорить и начать делать.» — Уолт Дисней",
            "«Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.» — Уинстон Черчилль",
            "«Единственный способ делать великие дела — любить то, что ты делаешь.» — Стив Джобс",
            "«Сложнее всего начать действовать, все остальное зависит только от упорства.» — Амелия Эрхарт",
            "«Мечты сбываются, когда мысли превращаются в действия.» — Дональд Трамп",
            "«Не бойся совершенства. Тебе его никогда не достичь.» — Сальвадор Дали"
        ]
        return random.choice(quotes)