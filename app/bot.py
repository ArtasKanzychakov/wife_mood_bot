# app/bot.py

from telegram.ext import Application
from app.config import BOT_TOKEN
from app.dispatcher import setup_handlers

def start_bot():
    app = Application.builder().token(BOT_TOKEN).build()
    setup_handlers(app)
    app.run_polling()

if __name__ == "__main__":
    start_bot()
