import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Основные настройки
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    ADMIN_ID = int(os.getenv('ADMIN_ID', 0))
    
    # БД
    POSTGRES_URL = os.getenv('POSTGRES_URL', 'sqlite:///bot.db')
    
    # Время
    REQUEST_TIMEOUT = 10
    PING_INTERVAL = 330  # 5.5 минут
    HEALTH_CHECK_INTERVAL = 660  # 11 минут
    
    # Парсинг
    CACHE_TIME = 300  # 5 минут кэша
    
    # Безопасность
    ALLOWED_IPS = [
        '149.154.160.0/20',
        '91.108.4.0/22'
    ]