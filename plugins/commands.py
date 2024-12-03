# © TechifyBots (Rahul)
import requests
import random
import asyncio
import string
import pytz
from datetime import datetime
from Script import script
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details
from database.users_chats_db import db
from info import ADMINS, THREE_VERIFY_GAP, LOG_CHANNEL, USERNAME, VERIFY_IMG, IS_VERIFY, AUTH_CHANNEL, SHORTENER_WEBSITE, SHORTENER_API, SHORTENER_WEBSITE2, SHORTENER_API2, SHORTENER_API3, SHORTENER_WEBSITE3, LOG_API_CHANNEL, TWO_VERIFY_GAP, TUTORIAL, TUTORIAL2, TUTORIAL3, QR_CODE, DELETE_TIME
from utils import get_settings, save_group_settings, is_subscribed, get_size, get_shortlink, is_check_admin, get_status, temp, get_readable_time
import re
import base64

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client:Client, message): 
    m = message
    user_id = m.from_user.id
    if len(m.command) == 2 and m.command[1].startswith('notcopy'):
        _, userid, verify_id, file_id = m.command[1].split("_", 3)
        user_id = int(userid)
        grp_id = temp.CHAT.get(user_id, 0)
        settings = await get_settings(grp_id)         
        verify_id_info = await db.get_verify_id_info(user_id, verify_id)
        if not verify_id_info or verify_id_info["verified"]:
            await message.reply("<b>ʟɪɴᴋ ᴇxᴘɪʀᴇᴅ ᴛʀʏ ᴀɢᴀɪɴ...</b>")
            return  
        ist_timezone = pytz.timezone('Asia/Kolkata')
        if await db.user_verified(user_id):
            key = "third_time_verified"
        else:
            key = "second_time_verified" if await db.is_user_verified(user_id) else "last_verified"
        current_time = datetime.now(tz=ist_timezone)
        result = await db.update_notcopy_user(user_id, {key:current_time})
        await db.update_verify_id_info(user_id, verify_id, {"verified":True})
        if key == "third_time_verified": 
            num = 3 
        else: 
            num =  2 if key == "second_time_verified" else 1 
        if key == "third_time_verified": 
            msg = script.THIRDT_VERIFY_COMPLETE_TEXT
        else:
            msg = script.SECOND_VERIFY_COMPLETE_TEXT if key == "second_time_verified" else script.VERIFY_COMPLETE_TEXT
        await client.send_message(settings['log'], script.VERIFIED_LOG_TEXT.format(m.from_user.mention, user_id, datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%d %B %Y'), num))
        btn = [[
            InlineKeyboardButton("✅ ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ ɢᴇᴛ ꜰɪʟᴇ ✅", url=f"https://telegram.me/{temp.U_NAME}?start=file_{grp_id}_{file_id}"),
        ]]
        reply_markup=InlineKeyboardMarkup(btn)
        await m.reply_photo(
            photo=(VERIFY_IMG),
            caption=msg.format(message.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return 
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        status = get_status()
        aks=await message.reply_text(f"<b>🔥 ʏᴇs {status},\nʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ??</b>")
        await asyncio.sleep(600)
        await aks.delete()
        await m.delete()
        if (str(message.chat.id)).startswith("-100") and not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            group_link = await message.chat.export_invite_link()
            user = message.from_user.mention if message.from_user else "Dear" 
            await client.send_message(LOG_CHANNEL, script.NEW_GROUP_TXT.format(message.chat.title, message.chat.id, message.chat.username, group_link, total, user))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.NEW_USER_TXT.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ⇆', url=f'http://telegram.me/{temp.U_NAME}?startgroup=start')
        ],[
            InlineKeyboardButton('⚙ ꜰᴇᴀᴛᴜʀᴇs', callback_data='features'),
            InlineKeyboardButton('💸 ᴘʀᴇᴍɪᴜᴍ', callback_data='buy_premium')
        ],[
            InlineKeyboardButton('🚫 ᴇᴀʀɴ ᴍᴏɴᴇʏ ᴡɪᴛʜ ʙᴏᴛ 🚫', callback_data='earn')
        ]]   
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return

    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help", "buy_premium"]:
        if message.command[1] == "buy_premium":
            btn = [[
                InlineKeyboardButton('📸 sᴇɴᴅ sᴄʀᴇᴇɴsʜᴏᴛ 📸', url=USERNAME)
            ],[
                InlineKeyboardButton('🗑 ᴄʟᴏsᴇ 🗑', callback_data='close_data')
            ]]            
            await message.reply_photo(
                photo=(QR_CODE),
                caption=script.PREMIUM_TEXT.format(message.from_user.mention),
                reply_markup=InlineKeyboardMarkup(btn)
            )
            return
        buttons = [[
            InlineKeyboardButton('⇆ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘs ⇆', url=f'http://t.me/{temp.U_NAME}?startgroup=start')
        ],[
            InlineKeyboardButton('⚙ ꜰᴇᴀᴛᴜʀᴇs', callback_data='features'),
            InlineKeyboardButton('💸 ᴘʀᴇᴍɪᴜᴍ', callback_data='buy_premium')
        ],[
            InlineKeyboardButton('🚫 ᴇᴀʀɴ ᴍᴏɴᴇʏ ᴡɪᴛʜ ʙᴏᴛ 🚫', callback_data='earn')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=script.START_TXT.format(message.from_user.mention, get_status(), message.from_user.id),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return

    data = message.command[1]
    try:
        pre, grp_id, file_id = data.split('_', 2)
    except:
        pre, grp_id, file_id = "", 0, data

    settings = await get_settings(int(data.split("_", 2)[1]))
    id = settings.get('fsub_id', AUTH_CHANNEL)
    channel = int(id)
    if settings.get('fsub_id', AUTH_CHANNEL) and not await is_subscribed(client, message.from_user.id, channel):
        invite_link = await client.create_chat_invite_link(channel)
        btn = [[
                InlineKeyboardButton("⛔️ ᴊᴏɪɴ ɴᴏᴡ ⛔️", url=invite_link.invite_link)
                ]]
        if message.command[1] != "subscribe":
            btn.append([InlineKeyboardButton("♻️ ᴛʀʏ ᴀɢᴀɪɴ ♻️", url=f"https://t.me/{temp.U_NAME}?start={message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text=script.FSUB_TXT.format(message.from_user.mention),
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode=enums.ParseMode.HTML
        )
        return
            
    user_id = m.from_user.id
    if not await db.has_premium_access(user_id):
        grp_id = int(grp_id)
        user_verified = await db.is_user_verified(user_id)
        settings = await get_settings(grp_id)
        is_second_shortener = await db.use_second_shortener(user_id, settings.get('verify_time', TWO_VERIFY_GAP)) 
        is_third_shortener = await db.use_third_shortener(user_id, settings.get('third_verify_time', THREE_VERIFY_GAP))
        if settings.get("is_verify", IS_VERIFY) and (not user_verified or is_second_shortener or is_third_shortener):
            verify_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))
            await db.create_verify_id(user_id, verify_id)
            temp.CHAT[user_id] = grp_id
            verify = await get_shortlink(f"https://telegram.me/{temp.U_NAME}?start=notcopy_{user_id}_{verify_id}_{file_id}", grp_id, is_second_shortener, is_third_shortener)
            if is_third_shortener:
                rahul = settings.get('tutorial_three', TUTORIAL3)
            else:
                rahul = settings.get('tutorial_two', TUTORIAL2) if is_second_shortener else settings.get('tutorial', TUTORIAL)
            buttons = [[
                InlineKeyboardButton(text="✅️ ᴠᴇʀɪꜰʏ ✅️", url=verify),
                InlineKeyboardButton(text="❗ ʜᴏᴡ ᴛᴏ ᴠᴇʀɪꜰʏ ❓", url=rahul)
            ]]
            reply_markup=InlineKeyboardMarkup(buttons)
            if await db.user_verified(user_id): 
                msg = script.THIRDT_VERIFICATION_TEXT
            else:            
                msg = script.SECOND_VERIFICATION_TEXT if is_second_shortener else script.VERIFICATION_TEXT
            d = await m.reply_text(
                text=msg.format(message.from_user.mention, get_status()),
                protect_content = True,
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            await asyncio.sleep(300) 
            await d.delete()
            await m.delete()
            return
            
    if data.startswith("allfiles"):
        _, grp_id, key = data.split("_", 2)
        files = temp.FILES_ID.get(key)
        if not files:
            await message.reply_text("<b>⚠️ ᴀʟʟ ꜰɪʟᴇs ɴᴏᴛ ꜰᴏᴜɴᴅ ⚠️</b>")
            return
        settings = await get_settings(int(grp_id))
        all_files = []
        for file in files:
            settings = await get_settings(int(grp_id))
            CAPTION = settings['caption']
            f_caption = CAPTION.format(
                file_name = file.file_name,
                file_size = get_size(file.file_size),
                file_caption=file.caption
            )
            btn=[[
                InlineKeyboardButton("ᴡᴀᴛᴄʜ ᴏɴʟɪɴᴇ 👀 / ꜰᴀsᴛ ᴅᴏᴡɴʟᴏᴀᴅ 📥", callback_data=f'stream#{file.file_id}')
            ]]
            dlt=await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file.file_id,
                caption=f_caption,
                protect_content=settings['file_secure'],
                reply_markup=InlineKeyboardMarkup(btn)
            )
            all_files.append(dlt)
        await asyncio.sleep(600)
        for dlt_file in all_files:
            await dlt_file.delete()
        t=await client.send_message(message.from_user.id, "<b>⚠️ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ꜰɪʟᴇ ɪs ᴅᴇʟᴇᴛᴇᴅ ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪɴ ʙᴏᴛ, ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴀɢᴀɪɴ ᴛʜᴇɴ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ ☺️</b>")
        await asyncio.sleep(120)
        await t.delete()
        return

    type_, grp_id, file_id = data.split("_", 2)
    files_ = await get_file_details(file_id)
    if not files_:
        return await message.reply('<b>⚠️ ꜰɪʟᴇs ɴᴏᴛ ꜰᴏᴜɴᴅ ⚠️</b>')
    files = files_[0]
    grp_id = int(grp_id)
    user_id = message.from_user.id
    settings = await get_settings(int(grp_id))
    if type_ != 'shortlink' and not settings.get("is_verify", IS_VERIFY):
        link = await get_shortlink(f"https://t.me/{temp.U_NAME}?start=shortlink_{user_id}_{file_id}", grp_id)
        mention = message.from_user.mention
        wish = get_status()
        name = files.file_name
        size = get_size(files.file_size)
        btn = [[
            InlineKeyboardButton("✅ ꜰɪʟᴇ ✅", url=link),
            InlineKeyboardButton("⁉️ ʜᴏᴡ ᴛᴏ ᴏᴘᴇɴ ⁉️", url=settings['tutorial'])
        ],[
            InlineKeyboardButton("😁 ʙᴜʏ ꜱᴜʙꜱᴄʀɪᴘᴛɪᴏɴ - ᴅɪʀᴇᴄᴛ ꜰɪʟᴇꜱ 😁", callback_data='buy_premium')
        ]]
        await message.reply(f"<b>ʜʏ {mention} {wish},</b>\n\n📂 𝐍𝐚𝐦𝐞 ➠  <code>{name}</code>\n\n♻️ 𝐒𝐢𝐳𝐞 ➠  {size}\n\n<b><i>ʏᴏᴜʀ ꜰɪʟᴇ ɪꜱ ʀᴇᴀᴅʏ, ᴘʟᴇᴀꜱᴇ ɢᴇᴛ ᴜꜱɪɴɢ ᴛʜɪꜱ ʟɪɴᴋ 😋.</i></b>", reply_markup=InlineKeyboardMarkup(btn), protect_content=True)
        return

    files_ = await get_file_details(file_id)           
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        return await message.reply('<b>⚠️ ᴀʟʟ ꜰɪʟᴇs ɴᴏᴛ ꜰᴏᴜɴᴅ ⚠️</b>')
    files = files_[0]
    settings = await get_settings(int(grp_id))
    CAPTION = settings['caption']
    f_caption = CAPTION.format(
        file_name = files.file_name,
        file_size = get_size(files.file_size),
        file_caption=files.caption
    )
    btn = [[
        InlineKeyboardButton("ᴡᴀᴛᴄʜ ᴏɴʟɪɴᴇ 👀 / ꜰᴀsᴛ ᴅᴏᴡɴʟᴏᴀᴅ 📥", callback_data=f'stream#{file_id}')
    ]]
    d=await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=settings['file_secure'],
        reply_markup=InlineKeyboardMarkup(btn)
    )
    await asyncio.sleep(600)
    await d.delete()
    r = await message.reply_text("<b>⚠️ ʏᴏᴜʀ ʀᴇǫᴜᴇsᴛᴇᴅ ꜰɪʟᴇ ɪs ᴅᴇʟᴇᴛᴇᴅ ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ, ɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴀɢᴀɪɴ ᴛʜᴇɴ sᴇᴀʀᴄʜ ᴀɢᴀɪɴ ☺️</b>")
    await asyncio.sleep(120)
    await r.delete()

@Client.on_message(filters.command('settings'))
async def settings(client, message):
    user_id = message.from_user.id if message.from_user else None
    if not user_id:
        return await message.reply("<b>💔 ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ʏᴏᴜ ᴄᴀɴ'ᴛ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ...</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<code>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ.</code>")
    grp_id = message.chat.id
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    settings = await get_settings(grp_id)
    title = message.chat.title
    if settings is not None:
            buttons = [[
                InlineKeyboardButton('ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ', callback_data=f'setgs#auto_filter#{settings["auto_filter"]}#{grp_id}'),
                InlineKeyboardButton('ᴏɴ ✔️' if settings["auto_filter"] else 'ᴏꜰꜰ ✗', callback_data=f'setgs#auto_filter#{settings["auto_filter"]}#{grp_id}')
            ],[
                InlineKeyboardButton('ꜰɪʟᴇ sᴇᴄᴜʀᴇ', callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}'),
                InlineKeyboardButton('ᴏɴ ✔️' if settings["file_secure"] else 'ᴏꜰꜰ ✗', callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}')
            ],[
                InlineKeyboardButton('ɪᴍᴅʙ', callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}'),
                InlineKeyboardButton('ᴏɴ ✔️' if settings["imdb"] else 'ᴏꜰꜰ ✗', callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}')
            ],[
                InlineKeyboardButton('sᴘᴇʟʟ ᴄʜᴇᴄᴋ', callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}'),
                InlineKeyboardButton('ᴏɴ ✔️' if settings["spell_check"] else 'ᴏꜰꜰ ✗', callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}')
            ],[
                InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ', callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}'),
                InlineKeyboardButton(f'{get_readable_time(DELETE_TIME)}' if settings["auto_delete"] else 'ᴏꜰꜰ ✗', callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}')
            ],[
                InlineKeyboardButton('ʀᴇsᴜʟᴛ ᴍᴏᴅᴇ', callback_data=f'setgs#link#{settings["link"]}#{str(grp_id)}'),
                InlineKeyboardButton('ʟɪɴᴋ' if settings["link"] else 'ʙᴜᴛᴛᴏɴ', callback_data=f'setgs#link#{settings["link"]}#{str(grp_id)}')
            ],[
                InlineKeyboardButton('ꜰɪʟᴇꜱ ᴍᴏᴅᴇ', callback_data=f'setgs#is_verify#{settings.get("is_verify", IS_VERIFY)}#{grp_id}'),
                InlineKeyboardButton('ᴠᴇʀɪꜰʏ' if settings.get("is_verify", IS_VERIFY) else 'ꜱʜᴏʀᴛʟɪɴᴋ', callback_data=f'setgs#is_verify#{settings.get("is_verify", IS_VERIFY)}#{grp_id}')
            ],[
                InlineKeyboardButton('☕️ ᴄʟᴏsᴇ ☕️', callback_data='close_data')
            ]]
            t=await message.reply_text(
                text=f"ᴄʜᴀɴɢᴇ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs ꜰᴏʀ <b>'{title}'</b> ᴀs ʏᴏᴜʀ ᴡɪsʜ ✨",
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.HTML
            )
    else:
        await message.reply_text('<b>ꜱᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ</b>')
        await asyncio.sleep(120)
        await t.delete() 

@Client.on_message(filters.command('template')) 
async def save_template(client, message):
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    try:
        template = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("ɪɴᴄᴏᴍᴘʟᴇᴛᴇ ᴄᴏᴍᴍᴀɴᴅ 😒")    
    await save_group_settings(grp_id, 'template', template)
    await message.reply_text(f"<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴛᴇᴍᴘʟᴀᴛᴇ ꜰᴏʀ {title} ᴛᴏ\n\n{template}</b>", disable_web_page_preview=True)
    
@Client.on_message(filters.command("send"))
async def send_msg(bot, message):
    if message.from_user.id not in ADMINS:
        await message.reply('<b>ᴏɴʟʏ ᴛʜᴇ ʙᴏᴛ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ...</b>')
        return
    if message.reply_to_message:
        target_ids = message.text.split(" ")[1:]
        if not target_ids:
            await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴏɴᴇ ᴏʀ ᴍᴏʀᴇ ᴜꜱᴇʀ ɪᴅꜱ ᴀꜱ ᴀ ꜱᴘᴀᴄᴇ...</b>")
            return
        out = "\n\n"
        success_count = 0
        try:
            users = await db.get_all_users()
            for target_id in target_ids:
                try:
                    user = await bot.get_users(target_id)
                    out += f"{user.id}\n"
                    await message.reply_to_message.copy(int(user.id))
                    success_count += 1
                except Exception as e:
                    out += f"‼️ ᴇʀʀᴏʀ ɪɴ ᴛʜɪꜱ ɪᴅ - <code>{target_id}</code> <code>{str(e)}</code>\n"
            await message.reply_text(f"<b>✅️ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴍᴇꜱꜱᴀɢᴇ ꜱᴇɴᴛ ɪɴ `{success_count}` ɪᴅ\n<code>{out}</code></b>")
        except Exception as e:
            await message.reply_text(f"<b>‼️ ᴇʀʀᴏʀ - <code>{e}</code></b>")
    else:
        await message.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴀꜱ ᴀ ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ ᴍᴇꜱꜱᴀɢᴇ, ꜰᴏʀ ᴇɢ - <code>/send userid1 userid2</code></b>")

@Client.on_message(filters.command('caption'))
async def save_caption(client, message):
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")
    try:
        caption = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("<b><u>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs - </b>\n<code>/caption Join [Here](https://telegram.me/MovieVillaYT)\n\nFILE : {file_name}\nSize : {file_size}</code>")
    await save_group_settings(grp_id, 'caption', caption)
    await message.reply_text(f"<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴄᴀᴘᴛɪᴏɴ ꜰᴏʀ {title} ᴛᴏ\n\n{caption}</b>", disable_web_page_preview=True) 
    
@Client.on_message(filters.command("tutorial"))
async def tutorial(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        await message.reply_text("<b>ᴏɴʟʏ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ 😂</b>")
        return
    try:
        tutorial = re.findall("(?P<url>https?://[^\s]+)", message.text)[0]
    except:
        return await message.reply_text("<b><u><i>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</i></u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs - </b>\n<code>/tutorial https://youtu.be/0c-i2Lol6LU</code>")
    reply = await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
    await save_group_settings(grpid, 'tutorial', tutorial)
    await reply.edit_text(f"<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴛᴜᴛᴏʀɪᴀʟ ꜰᴏʀ {title}</b>\n\nʟɪɴᴋ - {tutorial}", disable_web_page_preview=True)

@Client.on_message(filters.command("tutorial2"))
async def tutorial_two(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        await message.reply_text("<b>ᴏɴʟʏ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ 😂</b>")
        return
    try:
        tutorial_two = re.findall("(?P<url>https?://[^\s]+)", message.text)[0]
    except:
        return await message.reply_text("<b><u><i>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</i></u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs - </b>\n<code>/tutorial2 https://youtu.be/GdaUbzxDTKs</code>")
    reply = await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
    await save_group_settings(grpid, 'tutorial_two', tutorial_two)
    await reply.edit_text(f"<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ 𝟸ɴᴅ ᴛᴜᴛᴏʀɪᴀʟ ꜰᴏʀ {title}</b>\n\nʟɪɴᴋ - {tutorial_two}", disable_web_page_preview=True)

@Client.on_message(filters.command("tutorial3"))
async def tutorial_three(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        await message.reply_text("<b>ᴏɴʟʏ ɢʀᴏᴜᴘ ᴏᴡɴᴇʀ ᴄᴀɴ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ 😂</b>")
        return
    try:
        tutorial_three = re.findall("(?P<url>https?://[^\s]+)", message.text)[0]
    except:
        return await message.reply_text("<b><u><i>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</i></u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs - </b>\n<code>/tutorial3 https://youtu.be/rddlpYLm0G0</code>")
    reply = await message.reply_text("<b>ᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
    await save_group_settings(grpid, 'tutorial_three', tutorial_three)
    await reply.edit_text(f"<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ 𝟹ʀᴅ ᴛᴜᴛᴏʀɪᴀʟ ꜰᴏʀ {title}</b>\n\nʟɪɴᴋ - {tutorial_three}", disable_web_page_preview=True)

@Client.on_message(filters.command('shortlink'))
async def set_shortner(c, m):
    grp_id = m.chat.id
    title = m.chat.title
    if not await is_check_admin(c, grp_id, m.from_user.id):
        return await m.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')        
    if len(m.text.split()) == 1:
        await m.reply("<b><u>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs -\n`/shortlink onepagelink.in 8c09653e5c38f84d1b76ad3197c5a023e53b494d`</b>")
        return        
    sts = await m.reply("<b>♻️ ᴄʜᴇᴄᴋɪɴɢ...</b>")
    await asyncio.sleep(1.2)
    await sts.delete()
    chat_type = m.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")
    try:
        URL = m.command[1]
        API = m.command[2]
        resp = requests.get(f'https://{URL}/api?api={API}&url=https://telegram.me/RahulReviewsYT').json()
        if resp['status'] == 'success':
            SHORT_LINK = resp['shortenedUrl']
        await save_group_settings(grp_id, 'shortner', URL)
        await save_group_settings(grp_id, 'api', API)
        await m.reply_text(f"<b>✅ <u>sᴜᴄᴄᴇssꜰᴜʟʟʏ ʏᴏᴜʀ sʜᴏʀᴛɴᴇʀ ɪs ᴀᴅᴅᴇᴅ</u>\n\nᴅᴇᴍᴏ - {SHORT_LINK}\n\nsɪᴛᴇ - `{URL}`\n\nᴀᴘɪ - `{API}`</b>", quote=True)
        user_id = m.from_user.id
        user_info = f"@{m.from_user.username}" if m.from_user.username else f"{m.from_user.mention}"
        link = (await c.get_chat(m.chat.id)).invite_link
        grp_link = f"[{m.chat.title}]({link})"
        log_message = f"#New_Shortner_Set_For_1st_Verify\n\nName - {user_info}\nId - `{user_id}`\n\nDomain name - {URL}\nApi - `{API}`\nGroup link - {grp_link}"
        await c.send_message(LOG_API_CHANNEL, log_message, disable_web_page_preview=True)
    except Exception as e:
        await save_group_settings(grp_id, 'shortner', SHORTENER_WEBSITE)
        await save_group_settings(grp_id, 'api', SHORTENER_API)
        await m.reply_text(f"<b><u>💢 ᴇʀʀᴏʀ ᴏᴄᴄᴏᴜʀᴇᴅ!!</u>\n\nᴀᴜᴛᴏ ᴀᴅᴅᴇᴅ ʙᴏᴛ ᴏᴡɴᴇʀ ᴅᴇꜰᴜʟᴛ sʜᴏʀᴛɴᴇʀ\n\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇɴ ᴜsᴇ ᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ ᴏʀ ᴀᴅᴅ ᴠᴀʟɪᴅ sʜᴏʀᴛʟɪɴᴋ ᴅᴏᴍᴀɪɴ ɴᴀᴍᴇ & ᴀᴘɪ\n\nʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴄᴏɴᴛᴀᴄᴛ ɪɴ ᴏᴜʀ <a href=https://telegram.me/NobiDeveloperSupport>sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ</a> ꜰᴏʀ ꜱᴏʟᴠɪɴɢ ᴛʜɪs ɪssᴜᴇ...\n\n💔 ᴇʀʀᴏʀ - <code>{e}</code></b>", quote=True)

@Client.on_message(filters.command('shortlink2'))
async def set_shortner_2(c, m):
    grp_id = m.chat.id
    title = m.chat.title
    if not await is_check_admin(c, grp_id, m.from_user.id):
        return await m.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    if len(m.text.split()) == 1:
        await m.reply("<b><u>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs -\n`/shortlink2 tnshort.net 0c8ebd63bfe9f67f9970b8767498ff60316b9b03`</b>")
        return
    sts = await m.reply("<b>♻️ ᴄʜᴇᴄᴋɪɴɢ...</b>")
    await asyncio.sleep(1.2)
    await sts.delete()
    chat_type = m.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")
    try:
        URL = m.command[1]
        API = m.command[2]
        resp = requests.get(f'https://{URL}/api?api={API}&url=https://telegram.me/TechifyBots').json()
        if resp['status'] == 'success':
            SHORT_LINK = resp['shortenedUrl']
        await save_group_settings(grp_id, 'shortner_two', URL)
        await save_group_settings(grp_id, 'api_two', API)
        await m.reply_text(f"<b>✅ <u>ʏᴏᴜʀ 𝟸ɴᴅ sʜᴏʀᴛɴᴇʀ ɪs ᴀᴅᴅᴇᴅ</u>\n\nᴅᴇᴍᴏ - {SHORT_LINK}\n\nsɪᴛᴇ - `{URL}`\n\nᴀᴘɪ - `{API}`</b>", quote=True)
        user_id = m.from_user.id
        user_info = f"@{m.from_user.username}" if m.from_user.username else f"{m.from_user.mention}"
        link = (await c.get_chat(m.chat.id)).invite_link
        grp_link = f"[{m.chat.title}]({link})"
        log_message = f"#New_Shortner_Set_For_2nd_Verify\n\nName - {user_info}\nId - `{user_id}`\n\nDomain name - {URL}\nApi - `{API}`\nGroup link - {grp_link}"
        await c.send_message(LOG_API_CHANNEL, log_message, disable_web_page_preview=True)
    except Exception as e:
        await save_group_settings(grp_id, 'shortner_two', SHORTENER_WEBSITE2)
        await save_group_settings(grp_id, 'api_two', SHORTENER_API2)
        await m.reply_text(f"<b><u>💢 ᴇʀʀᴏʀ ᴏᴄᴄᴏᴜʀᴇᴅ!!</u>\n\nᴀᴜᴛᴏ ᴀᴅᴅᴇᴅ ʙᴏᴛ ᴏᴡɴᴇʀ ᴅᴇꜰᴜʟᴛ sʜᴏʀᴛɴᴇʀ\n\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇɴ ᴜsᴇ ᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ ᴏʀ ᴀᴅᴅ ᴠᴀʟɪᴅ sʜᴏʀᴛʟɪɴᴋ ᴅᴏᴍᴀɪɴ ɴᴀᴍᴇ & ᴀᴘɪ\n\nʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴄᴏɴᴛᴀᴄᴛ ɪɴ ᴏᴜʀ <a href=https://telegram.me/NobiDeveloperSupport>sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ</a> ꜰᴏʀ ꜱᴏʟᴠɪɴɢ ᴛʜɪs ɪssᴜᴇ...\n\n💔 ᴇʀʀᴏʀ - <code>{e}</code></b>", quote=True)

@Client.on_message(filters.command('log'))
async def set_log(client, message):
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    if len(message.text.split()) == 1:
        await message.reply("<b><u>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs -\n`/log -100xxxxxxxx`</b>")
        return
    sts = await message.reply("<b>♻️ ᴄʜᴇᴄᴋɪɴɢ...</b>")
    await asyncio.sleep(1.2)
    await sts.delete()
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")
    try:
        log = int(message.text.split(" ", 1)[1])
    except IndexError:
        return await message.reply_text("<b><u>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs -\n`/log -100xxxxxxxx`</b>")
    except ValueError:
        return await message.reply_text('<b>ᴍᴀᴋᴇ sᴜʀᴇ ɪᴅ ɪs ɪɴᴛᴇɢᴇʀ...</b>')
    try:
        t = await client.send_message(chat_id=log, text="<b>ʜᴇʏ ᴡʜᴀᴛ's ᴜᴘ!!</b>")
        await asyncio.sleep(3)
        await t.delete()
    except Exception as e:
        return await message.reply_text(f'<b><u>😐 ᴍᴀᴋᴇ sᴜʀᴇ ᴛʜɪs ʙᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ...</u>\n\n💔 ᴇʀʀᴏʀ - <code>{e}</code></b>')
    await save_group_settings(grp_id, 'log', log)
    await message.reply_text(f"<b>✅ sᴜᴄᴄᴇssꜰᴜʟʟʏ sᴇᴛ ʏᴏᴜʀ ʟᴏɢ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ {title}\n\nɪᴅ `{log}`</b>", disable_web_page_preview=True)
    user_id = message.from_user.id
    user_info = f"@{message.from_user.username}" if message.from_user.username else f"{message.from_user.mention}"
    link = (await client.get_chat(message.chat.id)).invite_link
    grp_link = f"[{message.chat.title}]({link})"
    log_message = f"#New_Log_Channel_Set\n\nName - {user_info}\nId - `{user_id}`\n\nLog channel id - `{log}`\nGroup link - {grp_link}"
    await client.send_message(LOG_API_CHANNEL, log_message, disable_web_page_preview=True)  

@Client.on_message(filters.command('ginfo'))
async def all_settings(client, message):
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")
    settings = await get_settings(grp_id)
    if not settings["is_verify"]:
        text = f"""<b><i><u>ᴄᴜʀʀᴇɴᴛ ᴠᴀʟᴜᴇꜱ ꜰᴏʀ {title}</u></i>

✅️ sʜᴏʀᴛɴᴇʀ ɴᴀᴍᴇ / ᴀᴘɪ
ɴᴀᴍᴇ : `{settings["shortner"]}`
ᴀᴘɪ : `{settings["api"]}`

🪄 ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ -
{settings.get('tutorial', TUTORIAL)}

🌀 ꜰꜱᴜʙ ᴄʜᴀɴɴᴇʟ ɪᴅ -
`{settings.get('fsub_id', AUTH_CHANNEL)}`

🎯 ɪᴍᴅʙ ᴛᴇᴍᴘʟᴀᴛᴇ -
`{settings['template']}`

📂 ꜰɪʟᴇ ᴄᴀᴘᴛɪᴏɴ - `{settings['caption']}`</b>"""
    else:
       text = f"""<b><i><u>ᴄᴜʀʀᴇɴᴛ ᴠᴀʟᴜᴇꜱ ꜰᴏʀ {title}</u></i>

✅️ 𝟷ꜱᴛ ꜱʜᴏʀᴛᴇɴᴇʀ ꜰᴏʀ ᴠᴇʀɪꜰʏ
ɴᴀᴍᴇ : `{settings["shortner"]}`
ᴀᴘɪ : `{settings["api"]}`

✅️ 𝟸ɴᴅ ꜱʜᴏʀᴛᴇɴᴇʀ ꜰᴏʀ ᴠᴇʀɪꜰʏ
ɴᴀᴍᴇ : `{settings["shortner_two"]}`
ᴀᴘɪ : `{settings["api_two"]}`

✅️ 𝟹ʀᴅ ꜱʜᴏʀᴛᴇɴᴇʀ ꜰᴏʀ ᴠᴇʀɪꜰʏ
ɴᴀᴍᴇ : `{settings["shortner_three"]}`
ᴀᴘɪ : `{settings["api_three"]}`

🧭 𝟸ɴᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ - `{settings['verify_time']}`

🧭 𝟹ʀᴅ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴛɪᴍᴇ - `{settings['third_verify_time']}`

1⃣ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ -
{settings.get('tutorial', TUTORIAL)}

2⃣ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ -
{settings.get('tutorial_two', TUTORIAL2)}

3⃣ ᴛᴜᴛᴏʀɪᴀʟ ʟɪɴᴋ -
{settings.get('tutorial_three', TUTORIAL3)}

📝 ʟᴏɢ ᴄʜᴀɴɴᴇʟ ɪᴅ -
`{settings['log']}`

🌀 ꜰꜱᴜʙ ᴄʜᴀɴɴᴇʟ ɪᴅ -
`{settings.get('fsub_id', AUTH_CHANNEL)}`

🎯 ɪᴍᴅʙ ᴛᴇᴍᴘʟᴀᴛᴇ -
`{settings['template']}`

📂 ꜰɪʟᴇ ᴄᴀᴘᴛɪᴏɴ - `{settings['caption']}`</b>""" 
    
    btn = [[
        InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close_data")
    ]]
    reply_markup=InlineKeyboardMarkup(btn)
    dlt=await message.reply_text(text, reply_markup=reply_markup, disable_web_page_preview=True)
    await asyncio.sleep(300)
    await dlt.delete()

@Client.on_message(filters.command('shortlink3'))
async def set_shortner_3(c, m):
    grp_id = m.chat.id
    title = m.chat.title
    if not await is_check_admin(c, grp_id, m.from_user.id):
        return await m.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    if len(m.text.split()) == 1:
        await m.reply("<b><u>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs -\n`/shortlink3 omegalinks.in 9c5a6c96077a1b499d8f953331221159383eb434`</b>")
        return
    sts = await m.reply("<b>♻️ ᴄʜᴇᴄᴋɪɴɢ...</b>")
    await asyncio.sleep(1.2)
    await sts.delete()
    chat_type = m.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await m.reply_text("<b>ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")
    try:
        URL = m.command[1]
        API = m.command[2]
        resp = requests.get(f'https://{URL}/api?api={API}&url=https://youtube.com/@RahulReviews').json()
        if resp['status'] == 'success':
            SHORT_LINK = resp['shortenedUrl']
        await save_group_settings(grp_id, 'shortner_three', URL)
        await save_group_settings(grp_id, 'api_three', API)
        await m.reply_text(f"<b>✅ <u>sᴜᴄᴄᴇssꜰᴜʟʟʏ ʏᴏᴜʀ 𝟹ʀᴅ sʜᴏʀᴛɴᴇʀ ɪs ᴀᴅᴅᴇᴅ</u>\n\nᴅᴇᴍᴏ - {SHORT_LINK}\n\nsɪᴛᴇ - `{URL}`\n\nᴀᴘɪ - `{API}`</b>", quote=True)
        user_id = m.from_user.id
        user_info = f"@{m.from_user.username}" if m.from_user.username else f"{m.from_user.mention}"
        link = (await c.get_chat(m.chat.id)).invite_link
        grp_link = f"[{m.chat.title}]({link})"
        log_message = f"#New_Shortner_Set_For_3rd_Verify\n\nName - {user_info}\nId - `{user_id}`\n\nDomain name - {URL}\nApi - `{API}`\nGroup link - {grp_link}"
        await c.send_message(LOG_API_CHANNEL, log_message, disable_web_page_preview=True)
    except Exception as e:
        await save_group_settings(grp_id, 'shortner_three', SHORTENER_WEBSITE3)
        await save_group_settings(grp_id, 'api_three', SHORTENER_API3)
        await m.reply_text(f"<b><u>💢 ᴇʀʀᴏʀ ᴏᴄᴄᴏᴜʀᴇᴅ!!</u>\n\nᴀᴜᴛᴏ ᴀᴅᴅᴇᴅ ʙᴏᴛ ᴏᴡɴᴇʀ ᴅᴇꜰᴜʟᴛ sʜᴏʀᴛɴᴇʀ\n\nɪꜰ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇɴ ᴜsᴇ ᴄᴏʀʀᴇᴄᴛ ꜰᴏʀᴍᴀᴛ ᴏʀ ᴀᴅᴅ ᴠᴀʟɪᴅ sʜᴏʀᴛʟɪɴᴋ ᴅᴏᴍᴀɪɴ ɴᴀᴍᴇ & ᴀᴘɪ\n\nʏᴏᴜ ᴄᴀɴ ᴀʟsᴏ ᴄᴏɴᴛᴀᴄᴛ ɪɴ ᴏᴜʀ <a href=https://telegram.me/NobiDeveloperSupport>sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ</a> ꜰᴏʀ ꜱᴏʟᴠɪɴɢ ᴛʜɪs ɪssᴜᴇ...\n\n💔 ᴇʀʀᴏʀ - <code>{e}</code></b>", quote=True)

@Client.on_message(filters.command('time2'))
async def set_time_2(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ...</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")       
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    try:
        time = int(message.text.split(" ", 1)[1])
    except:
        return await message.reply_text("<b><u>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs - </b>`/time2 1800`")
    await save_group_settings(grp_id, 'verify_time', time)
    await message.reply_text(f"<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ sᴇᴛ 𝟸ɴᴅ ᴠᴇʀɪꜰʏ ᴛɪᴍᴇ ꜰᴏʀ {title}\n\nᴛɪᴍᴇ - <code>{time} sec</code></b>")

@Client.on_message(filters.command('time3'))
async def set_time_3(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply("<b>ʏᴏᴜ ᴀʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ...</b>")
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")       
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    try:
        time = int(message.text.split(" ", 1)[1])
    except:
        return await message.reply_text("<b><u>ɪɴᴠᴀɪʟᴅ ꜰᴏʀᴍᴀᴛ!!</u>\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs - </b>`/time3 3600`")
    await save_group_settings(grp_id, 'third_verify_time', time)
    await message.reply_text(f"<b>sᴜᴄᴄᴇssꜰᴜʟʟʏ sᴇᴛ 𝟹ʀᴅ ᴠᴇʀɪꜰʏ ᴛɪᴍᴇ ꜰᴏʀ {title}\n\nᴛɪᴍᴇ - <code>{time} sec</code></b>")

@Client.on_message(filters.command('fsub'))
async def set_fsub(client, message):
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    try:
        channel_id = int(message.text.split(" ", 1)[1])
    except IndexError:
        return await message.reply_text("<b>ᴄᴏᴍᴍᴀɴᴅ ɪɴᴄᴏᴍᴘʟᴇᴛᴇ\n\nᴜsᴇ ʟɪᴋᴇ ᴛʜɪs -\n`/fsub -100xxxxxxxx`</b>")
    except ValueError:
        return await message.reply_text('<b>ᴍᴀᴋᴇ ꜱᴜʀᴇ ᴛʜᴇ ɪᴅ ɪꜱ ᴀɴ ɪɴᴛᴇɢᴇʀ.</b>')
    try:
        chat = await client.get_chat(channel_id)
    except Exception as e:
        return await message.reply_text(f"<b><code>{channel_id}</code> ɪꜱ ɪɴᴠᴀʟɪᴅ. ᴍᴀᴋᴇ ꜱᴜʀᴇ <a href=https://telegram.me/{temp.B_LINK}</a> ɪꜱ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴀᴛ ᴄʜᴀɴɴᴇʟ\n\n<code>{e}</code></b>")
    if chat.type != enums.ChatType.CHANNEL:
        return await message.reply_text(f"🫥 <code>{channel_id}</code> ᴛʜɪꜱ ɪꜱ ɴᴏᴛ ᴄʜᴀɴɴᴇʟ, ꜱᴇɴᴅ ᴍᴇ ᴏɴʟʏ ᴄʜᴀɴɴᴇʟ ɪᴅ ɴᴏᴛ ɢʀᴏᴜᴘ ɪᴅ</b>")
    await save_group_settings(grp_id, 'fsub_id', channel_id)
    mention = message.from_user.mention
    await client.send_message(LOG_CHANNEL, f"#Fsub_Channel_set\n\nUser - {mention} set the force channel for {title}:\n\nFsub channel - {chat.title}\nId - `{channel_id}`")
    await message.reply_text(f"<b>ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ꜱᴇᴛ ꜰᴏʀᴄᴇ ꜱᴜʙꜱᴄʀɪʙᴇ ᴄʜᴀɴɴᴇʟ ꜰᴏʀ {title}\n\nᴄʜᴀɴɴᴇʟ ɴᴀᴍᴇ - {chat.title}\nɪᴅ <code>{channel_id}</code></b>")

@Client.on_message(filters.command('nofsub'))
async def remove_fsub(client, message):
    chat_type = message.chat.type
    if chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        return await message.reply_text("<b>ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪɴ ɢʀᴏᴜᴘ...</b>")       
    grp_id = message.chat.id
    title = message.chat.title
    if not await is_check_admin(client, grp_id, message.from_user.id):
        return await message.reply_text('<b>ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴅᴍɪɴ ɪɴ ᴛʜɪꜱ ɢʀᴏᴜᴘ</b>')
    settings = await get_settings(grp_id)
    if settings.get('fsub_id', AUTH_CHANNEL) == AUTH_CHANNEL:
        await message.reply_text("<b>ʏᴏᴜ ʜᴀᴠᴇɴ'ᴛ sᴇᴛ ᴀɴʏ ꜰsᴜʙ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ 🤪\nᴛʜᴇɴ ʜᴏᴡ ᴄᴀɴ ʏᴏᴜ ʀᴇᴍᴏᴠᴇ ɪᴛ</b>")
    else:
        await save_group_settings(grp_id, 'fsub_id', AUTH_CHANNEL)
        mention = message.from_user.mention
        await client.send_message(LOG_CHANNEL, f"#Remove_Fsub_Channel\n\nUser - {mention} he remove fsub channel from {title}")
        await message.reply_text("<b>✅ sᴜᴄᴄᴇssꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ꜰᴏʀᴄᴇ ꜱᴜʙ ᴄʜᴀɴɴᴇʟ.</b>")

@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'Tʜɪs ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ɪɴᴅᴇxᴇᴅ ғɪʟᴇs.\nDᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ?',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Yᴇs", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Cᴀɴᴄᴇʟ", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )

@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer("Eᴠᴇʀʏᴛʜɪɴɢ's Gᴏɴᴇ")
    await message.message.edit('Sᴜᴄᴄᴇsғᴜʟʟʏ Dᴇʟᴇᴛᴇᴅ Aʟʟ Tʜᴇ Iɴᴅᴇxᴇᴅ Fɪʟᴇs.')

@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, Tʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏɴ'ᴛ ᴡᴏʀᴋ ɪɴ ɢʀᴏᴜᴘs. Iᴛ ᴏɴʟʏ ᴡᴏʀᴋs ᴏɴ ᴍʏ PM!</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hᴇʏ {message.from_user.mention}, Gɪᴠᴇ ᴍᴇ ᴀ ᴋᴇʏᴡᴏʀᴅ ᴀʟᴏɴɢ ᴡɪᴛʜ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴇʟᴇᴛᴇ ғɪʟᴇs.</b>")
    btn = [[
       InlineKeyboardButton("Yᴇs, Cᴏɴᴛɪɴᴜᴇ !", callback_data=f"techifybots#{keyword}")
       ],[
       InlineKeyboardButton("Nᴏ, Aʙᴏʀᴛ ᴏᴘᴇʀᴀᴛɪᴏɴ !", callback_data="close_data")
    ]]
    await message.reply_text(
        text="<b>Aʀᴇ ʏᴏᴜ sᴜʀᴇ? Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ?\n\nNᴏᴛᴇ:- Tʜɪs ᴄᴏᴜʟᴅ ʙᴇ ᴀ ᴅᴇsᴛʀᴜᴄᴛɪᴠᴇ ᴀᴄᴛɪᴏɴ!</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command("donate"))
async def donation(bot, message):
    btn = [[
        InlineKeyboardButton(text="❌   ᴄʟᴏsᴇ   ❌", callback_data="close_data")
    ]]
    yt=await message.reply_photo(photo='https://envs.sh/wam.jpg', caption=script.DONATE_TXT, reply_markup=InlineKeyboardMarkup(btn))
    await asyncio.sleep(300)
    await yt.delete()
    await message.delete()
