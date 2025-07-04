import asyncio
import logging

from dotenv import load_dotenv
from telethon import TelegramClient 

import bot.handlers as handlers
import bot.events as events
from bot.config.settings import Config
from bot.config.cache import Cache
from bot.database.database import Database
from bot.controllers.service import DataService
from bot.controllers.comment import CommentQueries
from bot.register_all import register

load_dotenv()
config = Config()
db = Database()

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
    handlers.register_all()
    
    events.client = client
    events.db = db
    events.register_all()
    
    service = await DataService.create(db)

    Cache.COMMENT_TEXT = await CommentQueries(db).get_comment_text()
    print(Cache.COMMENT_TEXT)
    
    await client.run_until_disconnected()
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())