from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from database.crud import create_user
from database.models import User
from datetime import datetime
import re

class Registration(StatesGroup):
    GET_NAME = State()
    GET_AGE = State()
    GET_BIRTH_DATE = State()
    CONFIRM_ZODIAC = State()

async def start_registration(message: types.Message):
    await message.answer("👋 Давай познакомимся! Как тебя зовут?")
    await Registration.GET_NAME.set()

async def process_name(message: types.Message, state: FSMContext):
    if not re.match(r"^[а-яА-ЯёЁa-zA-Z]{2,50}$", message.text):
        await message.answer("Пожалуйста, введите корректное имя (только буквы)")
        return
    
    await state.update_data(name=message.text)
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("18-25", "26-35", "36+")
    
    await message.answer("Сколько тебе лет?", reply_markup=markup)
    await Registration.GET_AGE.set()

async def process_age(message: types.Message, state: FSMContext):
    age_groups = {"18-25": 25, "26-35": 35, "36+": 36}
    if message.text not in age_groups:
        await message.answer("Пожалуйста, выберите вариант из клавиатуры")
        return
    
    await state.update_data(age=age_groups[message.text])
    
    await message.answer("Введите дату рождения в формате ДД.ММ.ГГГГ", 
                         reply_markup=types.ReplyKeyboardRemove())
    await Registration.GET_BIRTH_DATE.set()

async def process_birth_date(message: types.Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        await message.answer("Неверный формат даты. Попробуйте снова (ДД.ММ.ГГГГ)")
        return
    
    zodiac = calculate_zodiac(birth_date)
    await state.update_data(birth_date=birth_date, zodiac=zinc(zodiac))
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Да", callback_data="confirm_zodiac_yes"),
               types.InlineKeyboardButton("Нет", callback_data="confirm_zodiac_no"))
    
    await message.answer(f"Ваш знак зодиака: {zodiac}. Верно?", reply_markup=markup)
    await Registration.CONFIRM_ZODIAC.set()

async def confirm_zodiac(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "confirm_zodiac_no":
        await callback.message.answer("Введите правильный знак зодиака:")
        return
    
    user_data = await state.get_data()
    await create_user(
        telegram_id=callback.from_user.id,
        name=user_data['name'],
        age=user_data['age'],
        birth_date=user_data['birth_date'],
        zodiac=user_data['zinc']
    )
    
    await callback.message.answer("✅ Регистрация завершена!")
    await state.finish()

def calculate_zodiac(birth_date):
    # Упрощенная логика определения знака зодиака
    dates_zodiac = [
        (120, 'Козерог'), (218, 'Водолей'), (320, 'Рыбы'),
        (420, 'Овен'), (521, 'Телец'), (621, 'Близнецы'),
        (722, 'Рак'), (823, 'Лев'), (923, 'Дева'),
        (1023, 'Весы'), (1122, 'Скорпион'), (1222, 'Стрелец'),
        (1231, 'Козерог')
    ]
    month_day = birth_date.month * 100 + birth_date.day
    return next(zodiac for limit, zodiac in dates_zodiac if month_day <= limit)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_registration, commands=["start"])
    dp.register_message_handler(process_name, state=Registration.GET_NAME)
    dp.register_message_handler(process_age, state=Registration.GET_AGE)
    dp.register_message_handler(process_birth_date, state=Registration.GET_BIRTH_DATE)
    dp.register_callback_query_handler(confirm_zodiac, 
                                     lambda c: c.data.startswith('confirm_zodiac_'),
                                     state=Registration.CONFIRM_ZODIAC)
