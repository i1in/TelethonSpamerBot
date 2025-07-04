import re
from typing import Union

from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.errors import UserNotParticipantError
from telethon.errors.rpcerrorlist import UsernameNotOccupiedError
    
class ChannelHandlerHelpers:
    
    def extract_name(url: str) -> str:
        return re.sub(r"(https?:\/\/)?t\.me\/", "", url)

    async def is_subscribed(client, channel) -> bool:
        try:
            await client(GetParticipantRequest(channel.full_chat.id, 'me'))
            return True
        except UserNotParticipantError:
            return False

    def get_arg(message: str) -> str:
        text_list = message.split()
        return text_list[1] if len(text_list) > 1 else ""

    def get_all_args(message: str) -> list:
        text_list = message.split()
        text_list.pop(0)
        return text_list
    
    async def is_username_exists(client, username) -> bool:
        try:
            await client(ResolveUsernameRequest(username))
            return True
        except UsernameNotOccupiedError:
            return False