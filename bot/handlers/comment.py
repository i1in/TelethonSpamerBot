from datetime import datetime
from telethon import events
from . import client, db

from bot.controllers.comment import CommentQueries
from bot.config.settings import Config as config
from bot.config.cache import Cache
from bot.utils.helper import ChannelHandlerHelpers as helper
from bot.handlers import register

db = CommentQueries(db)

@register(events.NewMessage(pattern='/set_comment'))
async def message_handler(event):
    if event.sender_id not in config.ALLOWED_USERS:
        return
    
    extracted_args = helper.get_all_args(event.message.message)

    comment_text = " ".join(extracted_args)
    if not comment_text or len(comment_text) > 1440:
        await event.reply(
            "Not enough length for comment text. \n" +
            "Length from 1 to 1440 symbols."
        )
        return

    await db.add_comment_text(comment_text)
    Cache.COMMENT_TEXT = comment_text
    
    await event.reply(f"""
Comment text has been changed successfully.
New text: `{Cache.COMMENT_TEXT}`
    """, parse_mode="md")