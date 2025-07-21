import aiohttp
import asyncio
import logging
from config.settings import Config
from datetime import datetime

class WakeupService:
    def __init__(self):
        self.ping_count = 0
        self.last_ping = None

    async def ping_server(self):
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    start_time = datetime.now()
                    async with session.get(
                        f"{Config.WEBHOOK_URL}/wakeup",
                        timeout=Config.REQUEST_TIMEOUT
                    ) as response:
                        if response.status == 200:
                            self.ping_count += 1
                            self.last_ping = datetime.now()
                            logging.info(
                                f"Ping #{self.ping_count} successful. "
                                f"Response time: {(datetime.now() - start_time).total_seconds():.2f}s"
                            )
                        else:
                            logging.error(f"Ping failed with status {response.status}")
            except Exception as e:
                logging.error(f"Ping error: {str(e)}")
            
            await asyncio.sleep(Config.PING_INTERVAL)

    def get_status(self):
        return {
            "ping_count": self.ping_count,
            "last_ping": self.last_ping.isoformat() if self.last_ping else None,
            "next_ping_in": Config.PING_INTERVAL - (
                (datetime.now() - self.last_ping).total_seconds() 
                if self.last_ping 
                else 0
            )
        }

wakeup_service = WakeupService()
