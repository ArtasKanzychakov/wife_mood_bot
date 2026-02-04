from aiogram.types import (
    ReplyKeyboardMarkup, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    KeyboardButton
)


def main_menu():
    """Главное меню"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🔮 Гороскоп"),
        KeyboardButton("📰 Новости"),
        KeyboardButton("🎵 Музыка"),
        KeyboardButton("📅 Календарь"),
        KeyboardButton("💬 Цитата дня"),
        KeyboardButton("⚙️ Настройки"),
        KeyboardButton("📊 Статус бота"),
        KeyboardButton("❤️ Избранное")
    )
    return markup


def horoscope_menu():
    """Меню гороскопа"""
    markup = InlineKeyboardMarkup(row_width=3)
    zodiacs = [
        '♈ Овен', '♉ Телец', '♊ Близнецы',
        '♋ Рак', '♌ Лев', '♍ Дева',
        '♎ Весы', '♏ Скорпион', '♐ Стрелец',
        '♑ Козерог', '♒ Водолей', '♓ Рыбы'
    ]
    
    for i in range(0, 12, 3):
        markup.row(
            InlineKeyboardButton(zodiacs[i], callback_data=f"zodiac_{i}"),
            InlineKeyboardButton(zodiacs[i+1], callback_data=f"zodiac_{i+1}"),
            InlineKeyboardButton(zodiacs[i+2], callback_data=f"zodiac_{i+2}")
        )
    
    markup.row(InlineKeyboardButton("🔙 Назад", callback_data="back_main"))
    return markup


def news_menu():
    """Меню новостей"""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("📈 Бизнес", callback_data="news_business"),
        InlineKeyboardButton("🌍 Политика", callback_data="news_politics"),
        InlineKeyboardButton("💼 Экономика", callback_data="news_economy"),
        InlineKeyboardButton("⚽ Спорт", callback_data="news_sport"),
        InlineKeyboardButton("🔄 Обновить", callback_data="news_refresh"),
        InlineKeyboardButton("🔙 Назад", callback_data="back_main")
    )
    return markup


def settings_menu():
    """Меню настроек"""
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🔔 Уведомления", callback_data="settings_notify"),
        InlineKeyboardButton("🕐 Часовой пояс", callback_data="settings_timezone"),
        InlineKeyboardButton("👤 Профиль", callback_data="settings_profile"),
        InlineKeyboardButton("🗑️ Удалить данные", callback_data="settings_delete"),
        InlineKeyboardButton("🔙 Назад", callback_data="back_main")
    )
    return markup


def back_button():
    """Кнопка назад"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="back_main"))
    return markup


def refresh_button(callback_prefix):
    """Кнопка обновления"""
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔄 Обновить", callback_data=f"{callback_prefix}_refresh"))
    return markup