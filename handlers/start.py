from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config.keyboards import main_menu
from database.crud import get_or_create_user, update_user
from datetime import datetime
import re


class Registration(StatesGroup):
    GET_NAME = State()
    GET_ZODIAC = State()


async def start_command(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    await show_typing(message.chat.id, message.bot)
    
    # Проверяем, есть ли пользователь в БД
    from database.crud import SessionLocal
    db = SessionLocal()
    
    user = get_or_create_user(
        db,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    db.close()
    
    if user.zodiac:
        # Пользователь уже зарегистрирован
        welcome_text = (
            f"✨ *С возвращением, {user.first_name or 'друг'}!*\n\n"
            f"Рад снова тебя видеть! 🤗\n\n"
            f"Твой знак зодиака: *{user.zodiac}*\n"
            f"Настроение сегодня? 😊"
        )
        
        await message.answer(
            welcome_text,
            parse_mode='Markdown',
            reply_markup=main_menu()
        )
        await state.finish()
    else:
        # Новая регистрация
        await message.answer(
            "👋 *Привет! Я бот для хорошего настроения!*\n\n"
            "Я буду каждый день радовать тебя:\n"
            "🔮 Гороскопами\n"
            "📰 Интересными новостями\n"
            "🎵 Музыкой\n"
            "💬 Мудрыми цитатами\n\n"
            "Давай познакомимся! Как тебя зовут?",
            parse_mode='Markdown'
        )
        await Registration.GET_NAME.set()


async def process_name(message: types.Message, state: FSMContext):
    """Обработка имени"""
    name = message.text.strip()
    
    if not re.match(r"^[а-яА-ЯёЁa-zA-Z]{2,50}$", name):
        await message.answer(
            "❌ Пожалуйста, введите корректное имя\n"
            "(только буквы, 2-50 символов)"
        )
        return
    
    await state.update_data(name=name)
    
    from config.keyboards import horoscope_menu
    await message.answer(
        f"Приятно познакомиться, *{name}*! 👋\n\n"
        "Теперь выбери свой знак зодиака:",
        parse_mode='Markdown',
        reply_markup=horoscope_menu()
    )
    await Registration.GET_ZODIAC.set()


async def process_zodiac(callback: types.CallbackQuery, state: FSMContext):
    """Обработка выбора знака зодиака"""
    zodiac_index = int(callback.data.split('_')[1])
    
    zodiacs = [
        '♈ Овен', '♉ Телец', '♊ Близнецы',
        '♋ Рак', '♌ Лев', '♍ Дева',
        '♎ Весы', '♏ Скорпион', '♐ Стрелец',
        '♑ Козерог', '♒ Водолей', '♓ Рыбы'
    ]
    
    zodiac = zodiacs[zodiac_index]
    user_data = await state.get_data()
    
    # Сохраняем в БД
    from database.crud import SessionLocal
    db = SessionLocal()
    
    update_user(
        db,
        telegram_id=callback.from_user.id,
        zodiac=zodiac
    )
    
    db.close()
    
    await callback.message.edit_text(
        f"✅ *Отлично! Регистрация завершена!*\n\n"
        f"Твой знак зодиака: *{zodiac}*\n\n"
        f"Теперь ты можешь пользоваться всеми функциями бота! 🎉",
        parse_mode='Markdown'
    )
    
    await callback.message.answer(
        "👇 Выбери нужный раздел в меню:",
        reply_markup=main_menu()
    )
    
    await state.finish()
    await callback.answer()


async def show_typing(chat_id, bot):
    """Показать статус 'печатает'"""
    await bot.send_chat_action(chat_id, 'typing')
    import asyncio
    await asyncio.sleep(0.3)


def register_handlers(dp: Dispatcher):
    """Регистрация обработчиков"""
    dp.register_message_handler(start_command, commands=["start", "menu"])
    dp.register_message_handler(process_name, state=Registration.GET_NAME)
    dp.register_callback_query_handler(
        process_zodiac,
        lambda c: c.data.startswith('zodiac_'),
        state=Registration.GET_ZODIAC
    )