# app/webhook.py

from telegram.ext import Application
from app.config import BOT_TOKEN, WEBHOOK_URL, PORT
from app.dispatcher import setup_handlers

import asyncio
import os
from aiohttp import web

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    setup_handlers(app)
    await app.bot.set_webhook(f"{WEBHOOK_URL}/webhook")
    await app.start()
    web_app = web.Application()
    web_app.router.add_post("/webhook", app.webhook_handler())
    runner = web.AppRunner(web_app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", PORT)
    await site.start()
    print(f"Running on {WEBHOOK_URL}")
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
