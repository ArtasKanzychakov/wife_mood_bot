import asyncio
import aiohttp
import logging
from datetime import datetime
from config.settings import Config
from config.keyboards import main_menu

logger = logging.getLogger(__name__)


class KeepAliveService:
    """Сервис поддержания активности бота"""
    
    def __init__(self, bot):
        self.bot = bot
        self.ping_count = 0
        self.health_count = 0
        self.last_ping = None
        self.last_health = None
        self.stats = {
            'start_time': datetime.now(),
            'requests_today': 0,
            'errors_today': 0
        }
    
    async def start(self):
        """Запустить сервисы поддержания активности"""
        logger.info("🚀 Starting keep-alive services...")
        
        # Уровень 1: Пинг каждые 5.5 минут
        asyncio.create_task(self._ping_service())
        
        # Уровень 2: Health-check каждые 11 минут
        asyncio.create_task(self._health_service())
        
        logger.info("✅ Keep-alive services started")
    
    async def _ping_service(self):
        """Уровень 1: Регулярные ping-запросы"""
        while True:
            try:
                await self._send_ping()
                self.ping_count += 1
                self.last_ping = datetime.now()
                
                logger.info(f"✅ Ping #{self.ping_count} sent at {self.last_ping.strftime('%H:%M:%S')}")
                
            except Exception as e:
                logger.error(f"❌ Ping failed: {e}")
            
            await asyncio.sleep(Config.PING_INTERVAL)
    
    async def _health_service(self):
        """Уровень 2: Health-check и тестовые сообщения"""
        while True:
            try:
                await self._send_health_check()
                self.health_count += 1
                self.last_health = datetime.now()
                
                # Каждое 3е health-check - тестовое сообщение админу
                if self.health_count % 3 == 0 and Config.ADMIN_ID:
                    await self._send_test_message()
                
                logger.info(f"🏥 Health-check #{self.health_count} completed")
                
            except Exception as e:
                logger.error(f"❌ Health-check failed: {e}")
            
            await asyncio.sleep(Config.HEALTH_CHECK_INTERVAL)
    
    async def _send_ping(self):
        """Отправить ping-запрос"""
        if not Config.WEBHOOK_URL:
            return
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{Config.WEBHOOK_URL}/wakeup",
                    timeout=Config.REQUEST_TIMEOUT
                ) as response:
                    if response.status != 200:
                        raise Exception(f"Status {response.status}")
        except Exception as e:
            logger.warning(f"Ping request failed: {e}")
            # Пробуем альтернативный URL
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(
                        Config.WEBHOOK_URL,
                        timeout=Config.REQUEST_TIMEOUT
                    ) as response:
                        if response.status != 200:
                            raise Exception(f"Alternative ping failed: {response.status}")
            except Exception as e2:
                logger.error(f"All ping attempts failed: {e2}")
                raise
    
    async def _send_health_check(self):
        """Выполнить полную проверку здоровья"""
        checks = [
            self._check_webhook(),
            self._check_database(),
            self._check_parsers()
        ]
        
        results = await asyncio.gather(*checks, return_exceptions=True)
        
        health_status = {
            'webhook': isinstance(results[0], bool) and results[0],
            'database': isinstance(results[1], bool) and results[1],
            'parsers': isinstance(results[2], bool) and results[2]
        }
        
        logger.info(f"Health status: {health_status}")
        return all(health_status.values())
    
    async def _check_webhook(self):
        """Проверить вебхук"""
        try:
            webhook_info = await self.bot.get_webhook_info()
            return webhook_info.url == f"{Config.WEBHOOK_URL}/webhook"
        except:
            return False
    
    async def _check_database(self):
        """Проверить подключение к БД"""
        try:
            from database.crud import SessionLocal
            db = SessionLocal()
            db.execute("SELECT 1")
            db.close()
            return True
        except:
            return False
    
    async def _check_parsers(self):
        """Проверить парсеры"""
        try:
            from parsers.quote_parser import QuoteParser
            parser = QuoteParser()
            quote = await parser.parse()
            await parser.close()
            return bool(quote and len(quote) > 10)
        except:
            return False
    
    async def _send_test_message(self):
        """Отправить тестовое сообщение админу"""
        if not Config.ADMIN_ID:
            return
        
        try:
            uptime = datetime.now() - self.stats['start_time']
            hours = uptime.seconds // 3600
            minutes = (uptime.seconds % 3600) // 60
            
            message = (
                f"🤖 *Тестовая рассылка*\n\n"
                f"Бот работает: {hours}ч {minutes}м\n"
                f"Ping-запросов: {self.ping_count}\n"
                f"Health-check: {self.health_count}\n"
                f"Последний: {self.last_ping.strftime('%H:%M:%S') if self.last_ping else 'Никогда'}\n\n"
                f"✅ Все системы в норме!"
            )
            
            await self.bot.send_message(
                Config.ADMIN_ID,
                message,
                parse_mode='Markdown',
                reply_markup=main_menu()
            )
            
            logger.info(f"📤 Test message sent to admin")
            
        except Exception as e:
            logger.error(f"Failed to send test message: {e}")
    
    def get_stats(self):
        """Получить статистику"""
        uptime = datetime.now() - self.stats['start_time']
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        
        return {
            'ping_count': self.ping_count,
            'health_count': self.health_count,
            'last_ping': self.last_ping.isoformat() if self.last_ping else None,
            'last_health': self.last_health.isoformat() if self.last_health else None,
            'uptime': f"{hours}ч {minutes}м",
            'requests_today': self.stats['requests_today'],
            'errors_today': self.stats['errors_today']
        }
    
    def increment_request(self):
        """Увеличить счетчик запросов"""
        self.stats['requests_today'] += 1
    
    def increment_error(self):
        """Увеличить счетчик ошибок"""
        self.stats['errors_today'] += 1