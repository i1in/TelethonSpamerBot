from typing import Union
from ..database.database import Database

class ChannelQueries:

    def __init__(self, db: Database):
        self.db = db

    async def add_channel(self, channel_id: int, channel_name: str, channel_url: str) -> bool:
        result = await self.db.fetch_one("SELECT EXISTS(SELECT 1 FROM channel WHERE channel_id = ?)", (channel_id,))
        
        if result[0] == 1 and result is not None:
            return False
        
        await self.db.execute(
            """
            INSERT INTO channel(channel_id, channel_name, channel_url)
            VALUES (?, ?, ?);
            """,
            params=(
                channel_id,
                channel_name,
                channel_url
            )
        )
        return True
    
    async def remove_channel(self, channel: Union[str, int]) -> bool:
        result = await self.db.fetch_one("SELECT EXISTS(SELECT 1 FROM channel WHERE channel_id = ? OR channel_url = ?)", (channel, channel))
        
        if result is None or result[0] == 0:
            return False
        
        await self.db.execute(
            """
            DELETE FROM channel WHERE channel_id = ? OR channel_url = ?;
            """,
            params=(
                channel,
                channel
            )
        )
        
    
    async def get_channel(self, channel: Union[str, int]) -> Union[bool, tuple]:
        result = await self.db.fetch_one(
            "SELECT channel_id, channel_name, channel_url, added_at FROM channel WHERE channel_id = ? OR channel_name = ? OR channel_url = ?", 
            params=(channel, channel, channel))
        
        if result is None:
            return False
        
        return result
    
    async def get_all_channels(self) -> Union[bool, list]:
        result = await self.db.fetch_all(
            "SELECT channel_id, channel_name, channel_url FROM channel", 
            params=())
        
        if result is None:
            return False
        
        return result