import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    POSTGRES_URL = os.getenv('POSTGRES_URL')
    ALLOWED_IPS = os.getenv('ALLOWED_IPS', '149.154.160.0/20').split(',')
    
    # API Keys
    GIPHY_KEY = os.getenv('GIPHY_API_KEY')
    UNSPLASH_KEY = os.getenv('UNSPLASH_ACCESS_KEY')
    YANDEX_MUSIC_KEY = os.getenv('YANDEX_MUSIC_TOKEN')
    NEWSAPI_KEY = os.getenv('NEWSAPI_KEY')
    
    # Timeouts
    REQUEST_TIMEOUT = 10
    PING_INTERVAL = 300  # 5 минут
