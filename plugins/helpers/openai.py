from info import S_GROUP, OPENAI_API
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import openai

openai.api_key = OPENAI_API

@Client.on_message(filters.command("openai"))
async def openai(client, message):
    if message.chat.id != S_GROUP:
        btn = [[
            InlineKeyboardButton('Support Group', url="https://telegram.me/BotszSupport")
        ]]
        return await message.reply("This command only working in support group.", reply_markup=InlineKeyboardMarkup(btn))
    try:
        text = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("Command Incomplete!\nUsage: /openai your_question")
    msg = await message.reply("Searching...")
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=text,
            max_tokens=2000
        )
        await msg.edit(f"User: {message.from_user.mention}\nQuery: <code>{text}</code>\n\nResults:\n\n<code>{response.choices[0].text}</code>")
    except Exception as e:
        await msg.edit(f'Error - <code>{e}</code>')