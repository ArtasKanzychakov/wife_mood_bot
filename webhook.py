from aiohttp import web
from aiogram import Bot
from config.settings import Config
import logging
from app import dp  # Добавлен импорт dp

routes = web.RouteTableDef()
bot = Bot(token=Config.BOT_TOKEN)

@routes.post('/webhook')
async def webhook_handler(request):
    # Проверка IP
    client_ip = request.remote
    if not any(client_ip in net for net in Config.ALLOWED_IPS):
        return web.Response(status=403)
    
    update = await request.json()
    await dp.process_update(update)
    return web.Response(status=200)

@routes.get('/wakeup')
async def wakeup_handler(request):
    return web.Response(text="OK")

async def setup_webhook():
    await bot.set_webhook(f"{Config.WEBHOOK_URL}/webhook")

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=10000)  # Render запускает сервер на 10000

from wakeup import wakeup_service
import asyncio

async def background_tasks(app):
    asyncio.create_task(wakeup_service.ping_server())

app.on_startup.append(background_tasks)

