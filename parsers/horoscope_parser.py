from .base_parser import BaseParser
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)


class HoroscopeParser(BaseParser):
    """Парсер гороскопов с horoscope.mail.ru"""
    
    ZODIAC_URLS = {
        'aries': 'oven/today/',
        'taurus': 'telec/today/',
        'gemini': 'bliznecy/today/',
        'cancer': 'rak/today/',
        'leo': 'lev/today/',
        'virgo': 'deva/today/',
        'libra': 'vesy/today/',
        'scorpio': 'scorpion/today/',
        'sagittarius': 'strelec/today/',
        'capricorn': 'kozerog/today/',
        'aquarius': 'vodoley/today/',
        'pisces': 'ryby/today/'
    }
    
    async def parse(self, zodiac_sign):
        """Получить гороскоп для знака зодиака"""
        cache_key = f"horoscope_{zodiac_sign}"
        cached = self.get_cached(cache_key)
        if cached:
            return cached
        
        zodiac_path = self.ZODIAC_URLS.get(zodiac_sign.lower())
        if not zodiac_path:
            return "❌ Неизвестный знак зодиака"
        
        url = f"https://horo.mail.ru/prediction/{zodiac_path}"
        html = await self.fetch_html(url)
        
        if not html:
            fallback = self._get_fallback_horoscope(zodiac_sign)
            self.set_cache(cache_key, fallback)
            return fallback
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            # Ищем основной текст гороскопа
            content_div = soup.find('div', class_='article__item')
            if content_div:
                text = content_div.get_text(strip=True)
                if len(text) > 100:
                    self.set_cache(cache_key, text)
                    return text
            
            # Альтернативный поиск
            for div_class in ['article__text', 'p-prediction', 'content']:
                element = soup.find('div', class_=div_class)
                if element:
                    text = element.get_text(strip=True)
                    if len(text) > 100:
                        self.set_cache(cache_key, text)
                        return text
            
            # Если не нашли
            fallback = self._get_fallback_horoscope(zodiac_sign)
            self.set_cache(cache_key, fallback)
            return fallback
            
        except Exception as e:
            logger.error(f"Parse error for {zodiac_sign}: {e}")
            fallback = self._get_fallback_horoscope(zodiac_sign)
            self.set_cache(cache_key, fallback)
            return fallback
    
    def _get_fallback_horoscope(self, zodiac_sign):
        """Fallback гороскоп"""
        zodiac_names = {
            'aries': '♈ Овен', 'taurus': '♉ Телец', 'gemini': '♊ Близнецы',
            'cancer': '♋ Рак', 'leo': '♌ Лев', 'virgo': '♍ Дева',
            'libra': '♎ Весы', 'scorpio': '♏ Скорпион', 'sagittarius': '♐ Стрелец',
            'capricorn': '♑ Козерог', 'aquarius': '♒ Водолей', 'pisces': '♓ Рыбы'
        }
        name = zodiac_names.get(zodiac_sign.lower(), zodiac_sign)
        
        fallbacks = [
            f"{name}: Сегодня удачный день для новых начинаний.",
            f"{name}: Время проявить инициативу в отношениях.",
            f"{name}: Обратите внимание на здоровье.",
            f"{name}: Финансовые вопросы требуют внимания.",
            f"{name}: Удачный день для общения и встреч."
        ]
        import random
        return random.choice(fallbacks)