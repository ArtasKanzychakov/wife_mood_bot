from aiohttp import web
from aiogram import Bot
from config.settings import Config
from app import dp  # Импорт диспетчера
from wakeup import wakeup_service
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

routes = web.RouteTableDef()
bot = Bot(token=Config.BOT_TOKEN)

@routes.post('/webhook')
async def webhook_handler(request):
    try:
        update = await request.json()
        await dp.process_update(update)
        return web.Response(status=200)
    except Exception as e:
        logging.error(f"Webhook handler error: {str(e)}")
        return web.Response(status=500)

@routes.get('/wakeup')
async def wakeup_handler(request):
    return web.Response(text="OK")

async def setup_webhook():
    await bot.set_webhook(f"{Config.WEBHOOK_URL}/webhook")
    logging.info(f"Webhook set to {Config.WEBHOOK_URL}/webhook")

async def background_tasks(app):
    asyncio.create_task(wakeup_service.ping_server())

app = web.Application()
app.add_routes(routes)
app.on_startup.append(background_tasks)
app.on_startup.append(lambda app: setup_webhook())

if __name__ == '__main__':
    web.run_app(app, port=10000)  # Render использует порт 10000
