from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from config.settings import Config

async def show_main_menu(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        "🔮 Гороскоп", "👗 Мода",
        "🎵 Музыка", "⚙️ Настройки",
        "📈 Бизнес", "🧘 ЛФК"
    )
    await message.answer("Главное меню:", reply_markup=markup)

async def handle_horoscope(message: types.Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("На сегодня", callback_data="horoscope_today"))
    markup.add(InlineKeyboardButton("На неделю", callback_data="horoscope_week"))
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="menu_back"))
    
    await message.answer("Выберите период гороскопа:", reply_markup=markup)

async def handle_settings(message: types.Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Уведомления", callback_data="settings_notify"))
    markup.add(InlineKeyboardButton("Часовой пояс", callback_data="settings_timezone"))
    markup.add(InlineKeyboardButton("🔙 Назад", callback_data="menu_back"))
    
    await message.answer("Настройки бота:", reply_markup=markup)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(show_main_menu, commands=["menu"])
    dp.register_message_handler(handle_horoscope, lambda msg: msg.text == "🔮 Гороскоп")
    dp.register_message_handler(handle_settings, lambda msg: msg.text == "⚙️ Настройки")
    dp.register_callback_query_handler(
        lambda cb: show_main_menu(cb.message),
        lambda cb: cb.data == "menu_back"
    )
