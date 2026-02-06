from aiogram import Dispatcher, types
from config.keyboards import (
    main_menu, horoscope_menu, news_menu, 
    settings_menu, back_button, refresh_button
)
from utils.formatters import (
    format_header, format_divider, format_time,
    format_news_item, format_horoscope, format_quote,
    format_user_profile, format_bot_status, add_typing_indicator
)
from parsers.horoscope_parser import HoroscopeParser
from parsers.news_parser import NewsParser
from parsers.quote_parser import QuoteParser
from database.crud import SessionLocal, get_or_create_user
import asyncio


async def show_main_menu_handler(message: types.Message):
    """Показать главное меню"""
    await show_typing(message.chat.id, message.bot)
    await message.answer(
        "✨ *Главное меню* ✨\n\n"
        "👇 Выбери интересующий раздел:",
        parse_mode='Markdown',
        reply_markup=main_menu()
    )


async def horoscope_handler(message: types.Message):
    """Обработчик гороскопа"""
    await show_typing(message.chat.id, message.bot)
    await message.answer(
        "🔮 *Выбери знак зодиака:*",
        parse_mode='Markdown',
        reply_markup=horoscope_menu()
    )


async def zodiac_callback(callback: types.CallbackQuery):
    """Обработчик выбора знака зодиака"""
    zodiac_index = int(callback.data.split('_')[1])
    zodiacs = [
        ('♈ Овен', 'aries'), ('♉ Телец', 'taurus'), ('♊ Близнецы', 'gemini'),
        ('♋ Рак', 'cancer'), ('♌ Лев', 'leo'), ('♍ Дева', 'virgo'),
        ('♎ Весы', 'libra'), ('♏ Скорпион', 'scorpio'), ('♐ Стрелец', 'sagittarius'),
        ('♑ Козерог', 'capricorn'), ('♒ Водолей', 'aquarius'), ('♓ Рыбы', 'pisces')
    ]
    
    zodiac_name, zodiac_sign = zodiacs[zodiac_index]
    
    # Показываем статус загрузки
    await callback.message.edit_text(
        f"🔮 *{zodiac_name}*\n\n"
        f"⌛ Загружаю гороскоп...",
        parse_mode='Markdown'
    )
    
    # Парсим гороскоп
    parser = HoroscopeParser()
    prediction = await parser.parse(zodiac_sign)
    await parser.close()
    
    # Форматируем ответ
    response = (
        f"{format_header('Гороскоп на сегодня', '🔮')}\n"
        f"{format_time()}\n"
        f"{format_divider()}\n"
        f"{format_horoscope(zodiac_name, prediction)}\n"
        f"{format_divider()}\n"
        f"✨ *Хорошего дня!* ✨"
    )
    
    await callback.message.edit_text(
        response,
        parse_mode='Markdown',
        reply_markup=refresh_button('zodiac')
    )
    await callback.answer()


async def news_handler(message: types.Message):
    """Обработчик новостей"""
    await show_typing(message.chat.id, message.bot)
    await message.answer(
        "📰 *Выбери категорию новостей:*",
        parse_mode='Markdown',
        reply_markup=news_menu()
    )


async def news_callback(callback: types.CallbackQuery):
    """Обработчик категорий новостей"""
    await callback.message.edit_text(
        "📰 *Новости*\n\n"
        "⌛ Загружаю свежие новости...",
        parse_mode='Markdown'
    )
    
    # Парсим новости
    parser = NewsParser()
    news_list = await parser.parse_business_news()
    await parser.close()
    
    # Форматируем ответ
    response = format_header("Свежие новости", "📰") + "\n"
    response += format_time() + "\n"
    response += format_divider()
    
    for i, news in enumerate(news_list[:5]):
        response += format_news_item(news, i)
        if i < len(news_list[:5]) - 1:
            response += "\n"
    
    response += format_divider()
    response += "📊 *Всего новостей:* " + str(len(news_list))
    
    await callback.message.edit_text(
        response,
        parse_mode='Markdown',
        reply_markup=refresh_button('news')
    )
    await callback.answer()


async def quote_handler(message: types.Message):
    """Обработчик цитаты дня"""
    await show_typing(message.chat.id, message.bot)
    
    # Парсим цитату
    parser = QuoteParser()
    quote = await parser.parse()
    await parser.close()
    
    response = (
        f"{format_header('Цитата дня', '💭')}\n"
        f"{format_time()}\n"
        f"{format_divider()}\n"
        f"{format_quote(quote)}\n"
        f"{format_divider()}\n"
        f"💫 *Пусть вдохновение не покидает тебя!* 💫"
    )
    
    await message.answer(
        response,
        parse_mode='Markdown',
        reply_markup=refresh_button('quote')
    )


async def settings_handler(message: types.Message):
    """Обработчик настроек"""
    await show_typing(message.chat.id, message.bot)
    await message.answer(
        "⚙️ *Настройки бота:*",
        parse_mode='Markdown',
        reply_markup=settings_menu()
    )


async def profile_handler(callback: types.CallbackQuery):
    """Обработчик профиля"""
    # Получаем данные пользователя
    db = SessionLocal()
    user = get_or_create_user(
        db,
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name,
        last_name=callback.from_user.last_name
    )
    db.close()
    
    # Форматируем профиль
    user_data = {
        'telegram_id': user.telegram_id,
        'first_name': user.first_name,
        'zodiac': user.zodiac,
        'notify_enabled': user.notify_enabled,
        'timezone': user.timezone,
        'created_at': user.created_at.strftime('%d.%m.%Y')
    }
    
    response = format_user_profile(user_data)
    
    await callback.message.edit_text(
        response,
        parse_mode='Markdown',
        reply_markup=back_button()
    )
    await callback.answer()


async def status_handler(message: types.Message):
    """Обработчик статуса бота"""
    await show_typing(message.chat.id, message.bot)
    
    # Получаем статистику из keep_alive (будет доступна позже)
    from main import keep_alive_service
    
    stats = {
        'users': 0,  # Нужно добавить подсчет пользователей
        'webhook_active': True,
        'last_ping': 'Только что',
        'cache_size': 0,
        'uptime': '0:00',
        'requests_today': 0
    }
    
    if keep_alive_service:
        keep_stats = keep_alive_service.get_stats()
        stats.update(keep_stats)
    
    response = format_bot_status(stats)
    
    await message.answer(
        response,
        parse_mode='Markdown',
        reply_markup=refresh_button('status')
    )


async def back_callback(callback: types.CallbackQuery):
    """Обработчик кнопки 'Назад'"""
    if callback.data == "back_main":
        await callback.message.edit_text(
            "✨ *Главное меню* ✨\n\n"
            "👇 Выбери интересующий раздел:",
            parse_mode='Markdown',
            reply_markup=main_menu()
        )
        await callback.answer()


async def refresh_callback(callback: types.CallbackQuery):
    """Обработчик кнопки 'Обновить'"""
    action = callback.data.replace('_refresh', '')
    
    if action == 'zodiac':
        await horoscope_handler(callback.message)
    elif action == 'news':
        await news_handler(callback.message)
    elif action == 'quote':
        await quote_handler(callback.message)
    elif action == 'status':
        await status_handler(callback.message)
    
    await callback.answer()


async def show_typing(chat_id, bot):
    """Показать статус 'печатает'"""
    await bot.send_chat_action(chat_id, 'typing')
    await asyncio.sleep(0.3)


def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков меню"""
    # Команды
    dp.register_message_handler(show_main_menu_handler, commands=["menu"])
    
    # Текстовые обработчики
    dp.register_message_handler(horoscope_handler, lambda msg: msg.text == "🔮 Гороскоп")
    dp.register_message_handler(news_handler, lambda msg: msg.text == "📰 Новости")
    dp.register_message_handler(quote_handler, lambda msg: msg.text == "💬 Цитата дня")
    dp.register_message_handler(settings_handler, lambda msg: msg.text == "⚙️ Настройки")
    dp.register_message_handler(status_handler, lambda msg: msg.text == "📊 Статус бота")
    dp.register_message_handler(show_main_menu_handler, lambda msg: msg.text == "❤️ Избранное")
    
    # Колбэк-обработчики
    dp.register_callback_query_handler(zodiac_callback, lambda c: c.data.startswith('zodiac_'))
    dp.register_callback_query_handler(news_callback, lambda c: c.data.startswith('news_'))
    dp.register_callback_query_handler(profile_handler, lambda c: c.data == "settings_profile")
    dp.register_callback_query_handler(back_callback, lambda c: c.data == "back_main")
    dp.register_callback_query_handler(refresh_callback, lambda c: c.data.endswith('_refresh'))