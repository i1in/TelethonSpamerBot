from datetime import datetime
from telethon import events
from telethon.tl.functions.channels import GetFullChannelRequest, JoinChannelRequest, LeaveChannelRequest
from . import client, db

from bot.controllers.channels import ChannelQueries
from bot.config.settings import Config as config
from bot.utils.helper import ChannelHandlerHelpers as helper
from bot.handlers import register

db = ChannelQueries(db)

@register(events.NewMessage(pattern='/sub'))
async def message_handler(event):
    if event.sender_id not in config.ALLOWED_USERS:
        return
    
    channel_url = helper.get_arg(event.message.message)
    
    if not str(channel_url).startswith(("t.me/", "https://t.me")):
        await event.reply("Need url like:\nt.me/example\nhttps://t.me/example")
        return
    
    extracted_url = helper.extract_name(channel_url)
    
    if extracted_url.startswith("+"):
        await event.reply("Might be this link from private chat/channel. Bot is temporarily unable to support that.")
        return
    
    if not await helper.is_username_exists(client, extracted_url):
        await event.reply("Channel not found. Check your link.")
        return 
    
    channel = await client(GetFullChannelRequest(extracted_url))
    
    if channel.chats[0].megagroup:
        await event.reply("Bot is temporarily unable to join groups.")
        return
    
    if await helper.is_subscribed(client, channel):
        await event.reply("Already subscribed to this channel.")
        return
    
    await client(JoinChannelRequest(extracted_url))
    await db.add_channel(
        channel.full_chat.id, 
        channel.chats[0].title, 
        channel_url
    )
    
    await event.reply(f"Subcribed to [{channel.chats[0].title}]({channel_url}) [{channel.full_chat.id}]", parse_mode="md")
    
@register(events.NewMessage(pattern='/all'))
async def message_handler(event):
    if event.sender_id not in config.ALLOWED_USERS:
        return
    
    query = await db.get_all_channels()
    channels = "\n".join(f"{index + 1}. [{channel[1]}]({channel[2]}) ID: `{channel[0]}`" for index, channel in enumerate(query)) if len(query) > 0 else "`Nothing...`"
    await event.reply("All subscribed channels: \n" + channels, parse_mode="md")
    
@register(events.NewMessage(pattern='/info'))
async def message_handler(event):
    if event.sender_id not in config.ALLOWED_USERS:
        return
    
    channel = helper.get_arg(event.message.message)
    query = await db.get_channel(channel)
    if not query:
        await event.reply(f"This name/id/link isn't found in database", parse_mode="md")
        return
    
    txt = "\n".join(f"{key}: {value}" for index, (key, value) in enumerate(zip(["ID", "Name", "URL"], query))) + f"\n{datetime.fromtimestamp(query[3])}"
    
    await event.reply(
        f"About {channel}:\n" + txt, 
        parse_mode="md"
    )
    
@register(events.NewMessage(pattern="/unsub"))
async def message_handler(event):
    if event.sender_id not in config.ALLOWED_USERS:
        return
    
    channel = helper.get_arg(event.message.message)
    query_find = await db.get_channel(channel)
    if not query_find:
        await event.reply(f"This id/link isn't found in database", parse_mode="md")
        return
    
    await client(LeaveChannelRequest(query_find[0]))
    await db.remove_channel(channel)
    
    await event.reply(
        f"Removed [{query_find[1]}]({query_find[2]}) from database.", 
        parse_mode="md"
    )

@register(events.NewMessage(pattern="/test"))
async def message_handler(event):
    print(db)