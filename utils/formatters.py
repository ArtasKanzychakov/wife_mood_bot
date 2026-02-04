from datetime import datetime
import random


def format_header(title: str, emoji: str = "✨") -> str:
    """Форматирование заголовка"""
    return f"{emoji} *{title}* {emoji}"


def format_divider(length: int = 30, symbol: str = "─") -> str:
    """Разделитель"""
    return f"\n{symbol * length}\n"


def format_time() -> str:
    """Текущее время красиво"""
    now = datetime.now()
    return now.strftime("📅 *%d.%m.%Y*  🕐 *%H:%M*")


def format_news_item(news: dict, index: int) -> str:
    """Форматирование новости"""
    emojis = ["📰", "📈", "💼", "💰", "🌍"]
    emoji = emojis[index % len(emojis)]
    return f"{emoji} *{news['title']}*\n`Источник: {news['source']}`\n"


def format_horoscope(zodiac: str, prediction: str) -> str:
    """Форматирование гороскопа"""
    zodiac_emojis = {
        'Овен': '♈', 'Телец': '♉', 'Близнецы': '♊',
        'Рак': '♋', 'Лев': '♌', 'Дева': '♍',
        'Весы': '♎', 'Скорпион': '♏', 'Стрелец': '♐',
        'Козерог': '♑', 'Водолей': '♒', 'Рыбы': '♓'
    }
    
    emoji = zodiac_emojis.get(zodiac.split()[-1] if ' ' in zodiac else zodiac, '✨')
    return f"{emoji} *{zodiaz}*\n\n{prediction}"


def format_quote(quote: str) -> str:
    """Форматирование цитаты"""
    quote_emojis = ["💭", "📖", "✨", "🌟", "💫"]
    emoji = random.choice(quote_emojis)
    return f"{emoji} *Цитата дня*\n\n{quote}"


def format_user_profile(user_data: dict) -> str:
    """Форматирование профиля пользователя"""
    return f"""
👤 *Ваш профиль*

📛 Имя: {user_data.get('first_name', 'Не указано')}
🆔 ID: `{user_data.get('telegram_id', '')}`
♈ Знак зодиака: {user_data.get('zodiac', 'Не указан')}
🔔 Уведомления: {'✅ Включены' if user_data.get('notify_enabled') else '❌ Выключены'}
🕐 Часовой пояс: {user_data.get('timezone', 'Europe/Moscow')}
📅 Зарегистрирован: {user_data.get('created_at', 'Неизвестно')}
    """.strip()


def format_bot_status(stats: dict) -> str:
    """Форматирование статуса бота"""
    return f"""
🤖 *Статус бота*

📊 Пользователей: {stats.get('users', 0)}
🔗 Вебхук: {'✅ Активен' if stats.get('webhook_active') else '❌ Неактивен'}
🔄 Последний пинг: {stats.get('last_ping', 'Никогда')}
💾 Кэш: {stats.get('cache_size', 0)} записей
⚡ Время работы: {stats.get('uptime', '0:00')}
📈 Запросов сегодня: {stats.get('requests_today', 0)}
    """.strip()


def add_typing_indicator(text: str) -> str:
    """Добавить индикатор печати"""
    typing_indicators = ["⌛", "⏳", "✍️", "📝"]
    indicator = random.choice(typing_indicators)
    return f"{indicator} {text}"