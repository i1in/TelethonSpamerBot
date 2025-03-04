import asyncio

from telethon import events
from . import client, db
from telethon.tl.functions.channels import GetFullChannelRequest
from utils.channels import ChannelHandlerHelpers as helper

async def get_channel_ids():
    return [i[0] for i in await db.get_all_channels()]

@client.on(events.NewMessage)
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
            message="example",
            comment_to=messages[0].id
        )
        print("Comment sent")
    else:
        print("The channel hasn't a conversation group.")

    