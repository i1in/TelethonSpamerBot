import aiosqlite, asyncio, logging
import os
from pathlib import Path
from dotenv import load_dotenv

from bot.config.settings import Config as config

load_dotenv()

class Database:
    _instance = None

    def __new__(cls, db_path=config.DB_PATH):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_path = db_path
            cls._instance._connection = None
            cls._instance._lock = asyncio.Lock()
        return cls._instance
    
    async def connect(self):
        async with self._lock:
            if self._connection is None:
                self._connection = await aiosqlite.connect(self.db_path)
    
    async def get_connection(self):
        if self._connection is None:
            await self.connect()
        return self._connection
    
    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None

    async def execute(self, query: str, params: tuple = ()):
        connect = await self.get_connection()
        try:
            async with connect.execute(query, params):
                await connect.commit()
            
        except Exception as e:
            logging.error("Execute error: ", e)
            raise

        finally:
            await self.close()
    
    async def fetch_one(self, query: str, params: tuple):
        connect = await self.get_connection()
        try:
            async with connect.execute(query, params) as cursor:
                return await cursor.fetchone()
        
        except Exception as e:
            logging.error("Error: ", e)
            raise
        
        finally:
            await self.close()

    async def fetch_all(self, query: str, params: tuple):
        connect = await self.get_connection()
        try:
            async with connect.execute(query, params) as cursor:
                return await cursor.fetchall()
        
        except Exception as e:
            logging.error("Fetch_all error: ", e)
            raise
            
        finally: 
            await self.close()

    

    