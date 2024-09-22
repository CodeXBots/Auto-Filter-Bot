from pyrogram.raw.types import UpdateBotStopped
from pyrogram.types import Update
from database.users_chats_db import db
import logging
from pyrogram import Client, ContinuePropagation

@Client.on_raw_update(group=-15)
async def blocked_user(_: Client, u: Update, __: dict, ___: dict):
    if not isinstance(u, UpdateBotStopped):
        raise ContinuePropagation
    if not u.stopped:
        return
    await db.delete_user(u.user_id)
    logging.info(f"{u.user_id} - Removed from Database, since blocked account.")
