from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import web
import logging
import os
from config.settings import Config

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=Config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Инициализация сервисов
keep_alive_service = None

# Регистрация хендлеров
async def register_handlers():
    """Регистрация всех обработчиков"""
    logger.info("📝 Registering handlers...")
    
    from handlers import start, menu
    
    # Регистрируем хендлеры
    start.register_handlers(dp)
    menu.register_handlers(dp)
    
    # Регистрируем обработчик неизвестных команд
    @dp.message_handler()
    async def unknown_command(message):
        await message.answer(
            "🤔 *Не понимаю команду*\n\n"
            "Попробуй использовать меню или команду /start",
            parse_mode='Markdown',
            reply_markup=menu.main_menu()
        )
    
    logger.info("✅ Handlers registered")

# Вебхук-обработчики
routes = web.RouteTableDef()

@routes.post('/webhook')
async def webhook_handler(request):
    """Обработчик вебхука от Telegram"""
    try:
        # Проверяем IP Telegram
        peername = request.transport.get_extra_info('peername')
        if peername:
            client_ip = peername[0]
            from ipaddress import ip_network, ip_address
            
            allowed = False
            for subnet in Config.ALLOWED_IPS:
                if ip_address(client_ip) in ip_network(subnet, strict=False):
                    allowed = True
                    break
            
            if not allowed:
                logger.warning(f"⛔ Blocked IP: {client_ip}")
                return web.Response(status=403)
        
        # Обрабатываем update
        update = await request.json()
        await dp.process_update(update)
        
        # Логируем запрос
        if keep_alive_service:
            keep_alive_service.increment_request()
        
        return web.Response(status=200)
        
    except Exception as e:
        logger.error(f"Webhook error: {str(e)}")
        
        if keep_alive_service:
            keep_alive_service.increment_error()
        
        return web.Response(status=500)

@routes.get('/webhook')
async def webhook_info(request):
    """Информация о вебхуке"""
    webhook_info = await bot.get_webhook_info()
    return web.Response(
        text=f"Webhook URL: {webhook_info.url}\n"
             f"Pending updates: {webhook_info.pending_update_count}\n"
             f"Last error: {webhook_info.last_error_date}\n"
             f"Last error message: {webhook_info.last_error_message}",
        status=200
    )

@routes.post('/set_webhook')
async def set_webhook_handler(request):
    """Установка вебхука (для админа)"""
    try:
        data = await request.json()
        secret_token = data.get('secret_token')
        expected_token = os.getenv('WEBHOOK_SECRET', 'default_secret')
        
        if secret_token != expected_token:
            return web.Response(status=403)
        
        await bot.set_webhook(
            url=f"{Config.WEBHOOK_URL}/webhook",
            allowed_updates=["message", "callback_query"]
        )
        
        logger.info("✅ Webhook set successfully")
        return web.Response(text="Webhook set", status=200)
        
    except Exception as e:
        logger.error(f"Set webhook error: {e}")
        return web.Response(status=500)

@routes.get('/wakeup')
async def wakeup_handler(request):
    """Эндпоинт для поддержания активности"""
    return web.Response(text="✅ Bot is alive")

@routes.get('/health')
async def health_handler(request):
    """Health-check эндпоинт"""
    try:
        # Проверяем подключение к БД
        from database.crud import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        
        # Проверяем статус вебхука
        webhook_info = await bot.get_webhook_info()
        
        health_status = {
            "status": "healthy",
            "webhook": webhook_info.url == f"{Config.WEBHOOK_URL}/webhook",
            "database": "connected",
            "timestamp": webhook_info.last_error_date or "No errors"
        }
        
        return web.json_response(health_status, status=200)
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return web.json_response(
            {"status": "unhealthy", "error": str(e)},
            status=500
        )

@routes.get('/')
async def root_handler(request):
    """Корневой эндпоинт"""
    return web.Response(text="🤖 Wife Mood Bot is running!")

# События приложения
async def on_startup(app):
    """Действия при старте приложения"""
    logger.info("🚀 Starting bot application...")
    
    # Регистрируем хендлеры
    await register_handlers()
    
    # Устанавливаем вебхук
    try:
        webhook_url = f"{Config.WEBHOOK_URL}/webhook"
        await bot.set_webhook(
            url=webhook_url,
            allowed_updates=["message", "callback_query"]
        )
        logger.info(f"✅ Webhook set to: {webhook_url}")
    except Exception as e:
        logger.error(f"❌ Failed to set webhook: {e}")
    
    # Запускаем сервисы
    from services.keep_alive import KeepAliveService
    global keep_alive_service
    keep_alive_service = KeepAliveService(bot)
    await keep_alive_service.start()
    
    logger.info("✅ Bot startup completed")

async def on_shutdown(app):
    """Действия при остановке приложения"""
    logger.info("🛑 Shutting down bot...")
    
    # Удаляем вебхук
    await bot.delete_webhook()
    
    # Закрываем сессии парсеров
    from parsers.horoscope_parser import HoroscopeParser
    from parsers.news_parser import NewsParser
    from parsers.quote_parser import QuoteParser
    
    parsers = [HoroscopeParser(), NewsParser(), QuoteParser()]
    for parser in parsers:
        await parser.close()
    
    logger.info("✅ Bot shutdown completed")

# Создание приложения
app = web.Application()
app.add_routes(routes)
app.on_startup.append(on_startup)
app.on_shutdown.append(on_shutdown)

# Запуск приложения
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"🌐 Starting server on port {port}")
    web.run_app(app, host='0.0.0.0', port=port)