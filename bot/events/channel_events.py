import asyncio

from telethon import events
from datetime import datetime

from . import client, db
from telethon.tl.functions.channels import GetFullChannelRequest
from bot.utils.helper import ChannelHandlerHelpers as helper
from bot.config.settings import Config as config
from bot.config.cache import Cache
from bot.controllers.channels import ChannelQueries
from bot.events import register

db = ChannelQueries(db)

async def get_channel_ids():
    return [i[0] for i in await db.get_all_channels()]

@register(events.NewMessage)
async def new_channel_post_handler(event):
    channels = await get_channel_ids()
    
    if not hasattr(event.message.to_id, 'channel_id'):
        return
    
    if event.message.to_id.channel_id not in channels:
        return
    
    entity = await client.get_entity(event.message.to_id.channel_id)
    messages = await client.get_messages(entity, limit=1)
    channel = await client(GetFullChannelRequest(entity))
    
    if channel.full_chat and channel.full_chat.linked_chat_id:
        await client.send_message(
            entity=channel.chats[0].username,
            message=Cache.COMMENT_TEXT,
            comment_to=messages[0].id
        )
        
        await client.send_message(
            entity=config.OWNER_USERNAME,
            message=f"Sent comment to **{channel.chats[0].username} \n**" +
            f"Post: https://t.me/{channel.chats[0].username}/{messages[0].id} \n" +
            f"At: {datetime.now()}"
            
        )
    else:
        print("The channel hasn't a conversation group.")

    