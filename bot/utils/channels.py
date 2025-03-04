import re
from typing import Union

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.errors import UserNotParticipantError
from telethon.errors.rpcerrorlist import UsernameNotOccupiedError

from bot.database.database import Database

class ChannelQueries(Database):

    def __init__(self):
        super().__init__()
    
    async def initTable(self):
        await self.execute(
            """
            CREATE TABLE if NOT EXISTS channel (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel_id INTEGER UNIQUE,
                channel_name TEXT,
                channel_url TEXT,
                added_at INTEGER DEFAULT (strftime('%s', 'now'))
            );
            """,
            params=()
        )

    async def add_channel(self, channel_id: int, channel_name: str, channel_url: str) -> bool:
        result = await self.fetch_one("SELECT EXISTS(SELECT 1 FROM channel WHERE channel_id = ?)", (channel_id,))
        
        if result[0] == 1 and result is not None:
            return False
        
        await self.execute(
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
        result = await self.fetch_one("SELECT EXISTS(SELECT 1 FROM channel WHERE channel_id = ? OR channel_url = ?)", (channel, channel))
        
        if result is None or result[0] == 0:
            return False
        
        await self.execute(
            """
            DELETE FROM channel WHERE channel_id = ? OR channel_url = ?;
            """,
            params=(
                channel,
                channel
            )
        )
        
    
    async def get_channel(self, channel: Union[str, int]) -> Union[bool, tuple]:
        result = await self.fetch_one(
            "SELECT channel_id, channel_name, channel_url, added_at FROM channel WHERE channel_id = ? OR channel_name = ? OR channel_url = ?", 
            params=(channel, channel, channel))
        
        if result is None:
            return False
        
        return result
    
    async def get_all_channels(self) -> Union[bool, list]:
        result = await self.fetch_all(
            "SELECT channel_id, channel_name, channel_url FROM channel", 
            params=())
        
        if result is None:
            return False
        
        return result
    
class ChannelHandlerHelpers:
    
    def extract_name(url: str) -> str:
        return re.sub(r"(https?:\/\/)?t\.me\/", "", url)

    async def is_subscribed(client, channel) -> bool:
        try:
            await client(GetParticipantRequest(channel.full_chat.id, 'me'))
            return True
        except UserNotParticipantError:
            return False

    def get_arg(message):
        text_list = message.split()
        return text_list[1] if len(text_list) > 1 else ""
    
    async def is_username_exists(client, username) -> bool:
        try:
            await client(ResolveUsernameRequest(username))
            return True
        except UsernameNotOccupiedError:
            return False