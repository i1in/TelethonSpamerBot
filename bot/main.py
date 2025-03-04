import asyncio
import logging
import handlers
import events

from dotenv import load_dotenv
from telethon import TelegramClient 
from bot.config.settings import Config
from bot.utils.channels import ChannelQueries
from bot.register_all import register

load_dotenv()
config = Config()
db = ChannelQueries()

async def main() -> None:
    client = TelegramClient(
        'new', 
        config.API_ID, 
        config.API_HASH,
        device_model="Windows",
        system_version="Windows 10 x64",
        app_version="1.3.3.7", 
        flood_sleep_threshold=3
    )   
    await client.start()
    
    handlers.client = client
    handlers.db = db
    
    events.client = client
    events.db = db
    
    await db.initTable()
    
    register()
    await client.run_until_disconnected()
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())