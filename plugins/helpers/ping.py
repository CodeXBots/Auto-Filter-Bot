"""Telegram Ping / Pong Speed
Syntax: .ping"""

import time
import random
from pyrogram import Client, filters
from info import COMMAND_HAND_LER
from plugins.helper_functions.cust_p_filters import f_onw_fliter

# -- Constants -- #
ALIVES = "ɪ  ᴀᴍ  ᴀʟᴡᴀʏꜱ  ᴀʟɪᴠᴇ  ꜰᴏʀ  ʏᴏᴜ\n\nᴄʜᴇᴄᴋᴏᴜᴛ /start  ꜰᴏʀ  ᴍᴏʀᴇ..." 
# -- Constants End -- #


@Client.on_message(filters.command("alive", COMMAND_HAND_LER) & f_onw_fliter)
async def check_alive(_, message):
    await message.reply_text(ALIVES)


@Client.on_message(filters.command("ping", COMMAND_HAND_LER) & f_onw_fliter)
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"<b>Pong!\n{time_taken_s:.3f} ms</b>")