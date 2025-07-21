# app/dispatcher.py

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

from modules import (
    horoscopes, moon_cycles, news, jokes, exercises,
    psychology, esoterica, recipes, fashion,
    investment_news, investment_abc, audio_affirmations
)

from app.utils import send_typing_action

def setup_handlers(app):

    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("гороскоп", send_horoscope))
    app.add_handler(CommandHandler("мудрость", send_psychology))
    app.add_handler(CommandHandler("блюдо", send_recipe))
    app.add_handler(CommandHandler("анекдот", send_joke))
    app.add_handler(CommandHandler("инвестиция", send_investment_abc))
    app.add_handler(CommandHandler("новость", send_news))
    app.add_handler(CommandHandler("аффирмация", send_affirmation))
    app.add_handler(CommandHandler("луна", send_moon))

    # Callback кнопки
    app.add_handler(CallbackQueryHandler(handle_button))

@send_typing_action
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔮 Гороскоп", callback_data="гороскоп"),
         InlineKeyboardButton("🌙 Луна", callback_data="луна")],
        [InlineKeyboardButton("🍲 Рецепт", callback_data="рецепт"),
         InlineKeyboardButton("📰 Новости", callback_data="новость")],
        [InlineKeyboardButton("💸 Инвестиция", callback_data="инвестиция"),
         InlineKeyboardButton("🧘 Психология", callback_data="психология")],
        [InlineKeyboardButton("🎧 Аффирмация", callback_data="аффирмация"),
         InlineKeyboardButton("😂 Анекдот", callback_data="анекдот")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я — твой вдохновляющий бот. Выбери, что хочешь получить 💖", reply_markup=reply_markup)

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    handlers = {
        "гороскоп": send_horoscope,
        "луна": send_moon,
        "рецепт": send_recipe,
        "новость": send_news,
        "психология": send_psychology,
        "анекдот": send_joke,
        "инвестиция": send_investment_abc,
        "аффирмация": send_affirmation
    }

    if data in handlers:
        await handlers[data](update, context, from_button=True)

# Отдельные функции
@send_typing_action
async def send_horoscope(update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False):
    text = await horoscopes.get_today_horoscope()
    await reply(update, text)

@send_typing_action
async def send_moon(update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False):
    text = await moon_cycles.get_today_moon_phase()
    await reply(update, text)

@send_typing_action
async def send_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False):
    text = await recipes.get_recipe()
    await reply(update, text)

@send_typing_action
async def send_news(update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False):
    text = await news.get_news()
    await reply(update, text)

@send_typing_action
async def send_psychology(update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False):
    text = await psychology.get_tip()
    await reply(update, text)

@send_typing_action
async def send_joke(update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False):
    text = await jokes.get_joke()
    await reply(update, text)

@send_typing_action
async def send_investment_abc(update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False):
    text = await investment_abc.get_tip()
    await reply(update, text)

@send_typing_action
async def send_affirmation(update: Update, context: ContextTypes.DEFAULT_TYPE, from_button=False):
    audio = await audio_affirmations.get_affirmation()
    await reply_audio(update, audio)

async def reply(update: Update, text: str):
    if update.message:
        await update.message.reply_text(text, reply_markup=back_buttons())
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, reply_markup=back_buttons())

async def reply_audio(update: Update, audio: str):
    if update.message:
        await update.message.reply_audio(audio=audio, reply_markup=back_buttons())
    elif update.callback_query:
        await update.callback_query.message.reply_audio(audio=audio, reply_markup=back_buttons())

def back_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Назад", callback_data="start"),
         InlineKeyboardButton("🔁 Другое", callback_data="повторить")]
    ])
