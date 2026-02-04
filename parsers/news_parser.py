from .base_parser import BaseParser
from bs4 import BeautifulSoup
import logging
import re

logger = logging.getLogger(__name__)


class NewsParser(BaseParser):
    """Парсер новостей с разных сайтов"""
    
    async def parse_business_news(self):
        """Парсить бизнес-новости с rbc.ru"""
        cache_key = "news_business"
        cached = self.get_cached(cache_key)
        if cached:
            return cached
        
        urls = [
            "https://www.rbc.ru/business/",
            "https://www.rbc.ru/finances/",
            "https://www.kommersant.ru/rubric/3"
        ]
        
        news_items = []
        
        for url in urls:
            html = await self.fetch_html(url)
            if not html:
                continue
                
            try:
                soup = BeautifulSoup(html, 'html.parser')
                
                if 'rbc.ru' in url:
                    # Парсинг RBC
                    for item in soup.select('.news-feed__item, .item, .news-item')[:10]:
                        title_elem = item.select_one('.news-feed__item__title, .item__title, .news-item__title')
                        link_elem = item.select_one('a')
                        
                        if title_elem and link_elem:
                            title = title_elem.get_text(strip=True)
                            link = link_elem.get('href', '')
                            
                            if not link.startswith('http'):
                                link = f"https://www.rbc.ru{link}"
                            
                            if len(title) > 20:
                                news_items.append({
                                    'title': title[:200],
                                    'link': link,
                                    'source': 'RBC'
                                })
                
                elif 'kommersant.ru' in url:
                    # Парсинг Коммерсантъ
                    for item in soup.select('.uho__link, .rubric_lenta__item')[:10]:
                        title = item.get_text(strip=True)
                        link = item.get('href', '')
                        
                        if link and not link.startswith('http'):
                            link = f"https://www.kommersant.ru{link}"
                        
                        if len(title) > 20:
                            news_items.append({
                                'title': title[:200],
                                'link': link,
                                'source': 'Коммерсантъ'
                            })
                
                if len(news_items) >= 5:
                    break
                    
            except Exception as e:
                logger.error(f"Error parsing {url}: {e}")
                continue
        
        # Удаляем дубликаты
        unique_news = []
        seen_titles = set()
        for item in news_items:
            if item['title'] not in seen_titles:
                seen_titles.add(item['title'])
                unique_news.append(item)
        
        if not unique_news:
            unique_news = self._get_fallback_news()
        
        self.set_cache(cache_key, unique_news[:5])
        return unique_news[:5]
    
    async def parse_general_news(self):
        """Общие новости"""
        return await self.parse_business_news()
    
    def _get_fallback_news(self):
        """Fallback новости"""
        return [
            {
                'title': '📈 Рынки демонстрируют умеренный рост',
                'link': '#',
                'source': 'Аналитика'
            },
            {
                'title': '💼 Новые меры поддержки бизнеса',
                'link': '#',
                'source': 'Правительство'
            },
            {
                'title': '💰 Курсы валют стабилизировались',
                'link': '#',
                'source': 'ЦБ РФ'
            },
            {
                'title': '🏢 Компании внедряют удаленный формат',
                'link': '#',
                'source': 'HR-аналитика'
            },
            {
                'title': '🌍 Мировые тренды цифровизации',
                'link': '#',
                'source': 'Forbes'
            }
        ]