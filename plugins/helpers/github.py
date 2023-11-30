import os
import requests
import pyrogram
import json
from pyrogram import Client as Koshik
from pyrogram import filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters

BUTTONS = InlineKeyboardMarkup([[InlineKeyboardButton('🎪  ꜱᴜʙꜱᴄʀɪʙᴇ ᴍʏ ʏᴛ ᴄʜᴀɴɴᴇʟ  🎪', url='https://youtube.com/@NobiDeveloper')]])

@Client.on_message(filters.command(["github"]))
async def github(bot, message):
    if len(message.command) != 2:
        await message.reply_text("𝗜𝗻𝗰𝗼𝗺𝗽𝗹𝗲𝘁𝗲 𝗖𝗼𝗺𝗺𝗮𝗻𝗱  🤪\n\n➥  𝐆𝐢𝐯𝐞 𝐦𝐞 𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞 𝐚𝐥𝐨𝐧𝐠 𝐰𝐢𝐭𝐡 𝐭𝐡𝐞 𝐜𝐨𝐦𝐦𝐚𝐧𝐝 !\n\n♻️  𝗘𝘅𝗮𝗺𝗽𝗹𝗲:\n\n `/github Nobideveloper`", quote=True)
        return
    await message.reply_chat_action(enums.ChatAction.TYPING)
    k = await message.reply_text("**Searching...⏳**", quote=True)    
    un = message.text.split(None, 1)[1]
    URL = f'https://api.github.com/users/{un}'
    request = requests.get(URL)
    result = request.json()
    username = result['login']
    url = result['html_url']
    name = result['name']
    company = result['company']
    bio = result['bio']
    created_at = result['created_at']
    avatar_url = result['avatar_url']
    blog = result['blog']
    location = result['location']
    repositories = result['public_repos']
    followers = result['followers']
    following = result['following']
    capy = f"""𝗚𝗶𝘁𝗛𝘂𝗯  𝗗𝗲𝘁𝗮𝗶𝗹𝘀 :-

**ɴᴀᴍᴇ -** `{name}`
**ʙɪᴏ -** `{bio}`
**ʙʟᴏɢ -** `{blog}`
**ʟɪɴᴋ -** [ᴄʟɪᴄᴋ ʜᴇʀᴇ]({url})
**ᴄᴏᴍᴘᴀɴʏ -** `{company}`
**ʟᴏᴄᴀᴛɪᴏɴ -** `{location}`
**ᴜꜱᴇʀɴᴀᴍᴇ -** `{username}`
**ꜰᴏʟʟᴏᴡᴇʀꜱ -** `{followers}`
**ꜰᴏʟʟᴏᴡɪɴɢ -** `{following}`
**ᴄʀᴇᴀᴛᴇᴅ ᴏɴ -** `{created_at}`
**ʀᴇᴘᴏꜱɪᴛᴏʀɪᴇꜱ -** `{repositories}`"""
    await message.reply_photo(photo=avatar_url, caption=capy, reply_markup=BUTTONS)
    await k.delete()