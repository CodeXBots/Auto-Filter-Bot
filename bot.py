from pyrogram import Client, __version__, filters
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import API_ID, API_HASH, ADMINS, BOT_TOKEN, LOG_CHANNEL, PORT, SUPPORT_GROUP
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from Script import script 
from datetime import date, datetime 
import datetime
import pytz
from aiohttp import web
from plugins import web_server, check_expired_premium
import asyncio
import time

class Bot(Client):
    def __init__(self):
        super().__init__(
            name='aks',
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            sleep_threshold=5,
            workers=150,
            plugins={"root": "plugins"}
        )
        
    async def start(self):
        st = time.time()
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        temp.B_LINK = me.mention
        self.username = '@' + me.username
        self.loop.create_task(check_expired_premium(self))
        print(f"{me.first_name} is started now ❤️")
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.datetime.now(tz)
        timee = now.strftime("%H:%M:%S %p") 
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()
        await self.send_message(chat_id=LOG_CHANNEL, text=f"<b>{me.mention} ʀᴇsᴛᴀʀᴛᴇᴅ 🤖\n\n📆 ᴅᴀᴛᴇ - <code>{today}</code>\n🕙 ᴛɪᴍᴇ - <code>{timee}</code>\n🌍 ᴛɪᴍᴇ ᴢᴏɴᴇ - <code>Asia/Kolkata</code></b>")
        await self.send_message(chat_id=SUPPORT_GROUP, text=f"<b>{me.mention} ʀᴇsᴛᴀʀᴛᴇᴅ 🤖</b>")
        tt = time.time() - st
        seconds = int(datetime.timedelta(seconds=tt).seconds)
        for admin in ADMINS:
            await self.send_message(chat_id=admin, text=f"<b>✅ ʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ\n🕥 ᴛɪᴍᴇ ᴛᴀᴋᴇɴ - <code>{seconds} sᴇᴄᴏɴᴅs</code></b>")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped.")
    
    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat sequentially.
        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_messages` in a loop, thus saving
        you from the hassle of setting up boilerplate code. It is useful for getting the whole chat messages with a
        single call.
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                
            limit (``int``):
                Identifier of the last message to be returned.
                
            offset (``int``, *optional*):
                Identifier of the first message to be returned.
                Defaults to 0.
        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.
        Example:
            .. code-block:: python
                for message in app.iter_messages("pyrogram", 1, 15000):
                    print(message.text)
        """
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1

app = Bot()
app.run()
