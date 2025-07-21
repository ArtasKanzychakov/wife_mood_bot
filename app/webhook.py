# app/webhook.py

import os
from telegram import Update
from telegram.ext import Application, CommandHandler
from dotenv import load_dotenv

from app.bot import main_handler
from app.scheduler import setup_scheduler, set_target_chat

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Инициализация приложения
application = Application.builder().token(BOT_TOKEN).build()

# Устанавливаем webhook
async def set_webhook():
    await application.bot.set_webhook(WEBHOOK_URL)

# Приветствие при старте
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я настроен и жду команды ✨")
    # Установка чата для планировщика
    set_target_chat(update.effective_chat.id)

# Добавление команд
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("go", main_handler))

# Планировщик
setup_scheduler(application)

# Запуск
if __name__ == '__main__':
    import asyncio

    async def run():
        await set_webhook()
        print("✅ Webhook установлен")
        await application.run_polling()  # Render использует WSGI — но Polling оставлен как fallback

    asyncio.run(run())
