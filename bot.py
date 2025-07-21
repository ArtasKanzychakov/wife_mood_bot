import os
import logging
from dotenv import load_dotenv

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputFile
)
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler
)

from app.scheduler import setup_scheduler, set_target_chat
from modules import (
    horoscopes, moon_cycles, jokes, psychology,
    esoterica, recipes, exercises, news,
    investment_news, investment_abc, audio_affirmations,
    fashion
)

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
PORT = int(os.getenv("PORT", "8443"))
HEROKU_APP_NAME = os.getenv("HEROKU_APP_NAME", "")
WEBHOOK_URL = f"https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}" if HEROKU_APP_NAME else None

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Основные кнопки и клавиатуры ---

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🌟 Гороскоп", callback_data="horoscope")],
        [InlineKeyboardButton("😂 Анекдот", callback_data="joke"),
         InlineKeyboardButton("🧠 Психология", callback_data="psychology")],
        [InlineKeyboardButton("🔮 Эзотерика", callback_data="esoterica"),
         InlineKeyboardButton("🍽 Блюдо дня", callback_data="recipe")],
        [InlineKeyboardButton("💼 Инвестиции", callback_data="investments")],
        [InlineKeyboardButton("🧘‍♀️ Упражнение", callback_data="exercise")],
        [InlineKeyboardButton("📰 Новости", callback_data="news"),
         InlineKeyboardButton("👗 Мода", callback_data="fashion")],
        [InlineKeyboardButton("🎧 Аффирмация", callback_data="affirmation")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_button_keyboard():
    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)

# --- Хендлеры команд ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    set_target_chat(chat_id)
    await update.message.reply_text(
        "Привет! Я бот для поднятия настроения твоей любимой. Выбирай интересующее:",
        reply_markup=main_menu_keyboard()
    )

# --- Обработка нажатий на кнопки ---

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "back":
        await query.edit_message_text(
            "Главное меню:",
            reply_markup=main_menu_keyboard()
        )
        return

    # Обработка по ключу
    if data == "horoscope":
        text = await horoscopes.get_today_horoscope()
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "joke":
        text = await jokes.get_joke()
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "psychology":
        text = await psychology.get_tip()
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "esoterica":
        text = await esoterica.get_tip()
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "recipe":
        text = await recipes.get_recipe()
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "investments":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Новости по инвестициям", callback_data="invest_news")],
            [InlineKeyboardButton("Азбука инвестиций", callback_data="invest_abc")],
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
        ])
        await query.edit_message_text("Выберите раздел:", reply_markup=keyboard)

    elif data == "invest_news":
        text = await investment_news.get_news()
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "invest_abc":
        text = await investment_abc.get_tip()
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "exercise":
        morning_ex = await exercises.get_morning_exercise()
        evening_ex = await exercises.get_evening_exercise()
        text = f"🧘‍♀️ Утреннее упражнение:\n{morning_ex}\n\n🌙 Вечернее упражнение:\n{evening_ex}"
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "news":
        text = await news.get_news()
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "fashion":
        text = await fashion.get_tip()
        await query.edit_message_text(text=text, reply_markup=back_button_keyboard())

    elif data == "affirmation":
        audio_url = await audio_affirmations.get_affirmation()
        await query.message.reply_audio(audio=audio_url)
        await query.edit_message_text(text="🎧 Вот твоя аффирмация!", reply_markup=back_button_keyboard())

# --- Закрепленные сообщения (пример) ---

async def pinned_message(context: ContextTypes.DEFAULT_TYPE):
    chat_id = context.job.chat_id
    text = (
        "✨ Добро пожаловать!\n"
        "Используйте кнопки ниже для выбора контента.\n"
        "Каждый час я буду присылать что-то интересное.\n"
        "Если нужно, всегда можно вернуться сюда."
    )
    await context.bot.send_message(chat_id, text=text, reply_markup=main_menu_keyboard())

# --- Основной запуск ---

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    setup_scheduler(app)  # запускаем планировщик

    if WEBHOOK_URL:
        # Запуск с webhook (Render, Heroku)
        await app.bot.set_webhook(WEBHOOK_URL)
        await app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            webhook_url=WEBHOOK_URL
        )
    else:
        # Локальный запуск polling
        await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
