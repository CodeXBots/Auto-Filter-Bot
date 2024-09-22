import asyncio
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery 
from plugins.helper.Rahul import Fonts

@Client.on_message(filters.private & filters.command(["font"]))
async def style_buttons(c, m, cb=False):
    try:
        title = m.text.split(" ", 1)[1]
    except IndexError:
        await m.reply_text(text="Enter any text. Example: /font [text]")
        return

    fonts = [
        Fonts.typewriter, Fonts.script, Fonts.outline, Fonts.serief, Fonts.bold_cool, Fonts.cool, Fonts.smallcap, Fonts.script, Fonts.bold_script, Fonts.tiny, Fonts.comic, Fonts.san, Fonts.slant_san, Fonts.slant, Fonts.sim, Fonts.circles, Fonts.dark_circle, Fonts.gothic, Fonts.bold_gothic, Fonts.cloud, Fonts.happy, Fonts.sad, Fonts.special, Fonts.square, Fonts.dark_square, Fonts.andalucia, Fonts.manga, Fonts.stinky, Fonts.bubbles, Fonts.underline, Fonts.ladybug, Fonts.rays, Fonts.birds, Fonts.slash, Fonts.stop, Fonts.skyline, Fonts.arrows, Fonts.rvnes, Fonts.strike, Fonts.frozen
    ]

    messages = []  # Store the messages to delete later

    for font in fonts:
        reply = await m.reply_text(f"{font(title)}")
        messages.append(reply)

    d=await m.reply_text(text="<b>ʙʏ : @RahulReviewsYT</b>")

    async def delete_messages():
        for msg in messages:
            await c.delete_messages(m.chat.id, msg.id)

    # Wait for 10 minutes before deleting the messages
    await asyncio.sleep(120)
    await delete_messages()
    await m.delete()
    await d.delete()

@Client.on_callback_query(filters.regex('^style'))
async def style(c, m):
    await m.answer()
    cmd, style = m.data.split('+')

    if style == 'typewriter':
        cls = Fonts.typewriter
    if style == 'outline':
        cls = Fonts.outline
    if style == 'serif':
        cls = Fonts.serief
    if style == 'bold_cool':
        cls = Fonts.bold_cool
    if style == 'cool':
        cls = Fonts.cool
    if style == 'small_cap':
        cls = Fonts.smallcap
    if style == 'script':
        cls = Fonts.script
    if style == 'script_bolt':
        cls = Fonts.bold_script
    if style == 'tiny':
        cls = Fonts.tiny
    if style == 'comic':
        cls = Fonts.comic
    if style == 'sans':
        cls = Fonts.san
    if style == 'slant_sans':
        cls = Fonts.slant_san
    if style == 'slant':
        cls = Fonts.slant
    if style == 'sim':
        cls = Fonts.sim
    if style == 'circles':
        cls = Fonts.circles
    if style == 'circle_dark':
        cls = Fonts.dark_circle
    if style == 'gothic':
        cls = Fonts.gothic
    if style == 'gothic_bolt':
        cls = Fonts.bold_gothic
    if style == 'cloud':
        cls = Fonts.cloud
    if style == 'happy':
        cls = Fonts.happy
    if style == 'sad':
        cls = Fonts.sad
    if style == 'special':
        cls = Fonts.special
    if style == 'squares':
        cls = Fonts.square
    if style == 'squares_bold':
        cls = Fonts.dark_square
    if style == 'andalucia':
        cls = Fonts.andalucia
    if style == 'manga':
        cls = Fonts.manga
    if style == 'stinky':
        cls = Fonts.stinky
    if style == 'bubbles':
        cls = Fonts.bubbles
    if style == 'underline':
        cls = Fonts.underline
    if style == 'ladybug':
        cls = Fonts.ladybug
    if style == 'rays':
        cls = Fonts.rays
    if style == 'birds':
        cls = Fonts.birds
    if style == 'slash':
        cls = Fonts.slash
    if style == 'stop':
        cls = Fonts.stop
    if style == 'skyline':
        cls = Fonts.skyline
    if style == 'arrows':
        cls = Fonts.arrows
    if style == 'qvnes':
        cls = Fonts.rvnes
    if style == 'strike':
        cls = Fonts.strike
    if style == 'frozen':
        cls = Fonts.frozen

    r, oldtxt = m.message.reply_to_message.text.split(None, 1) 
    new_text = cls(oldtxt)            
    try:
        await m.message.edit_text(f"`{new_text}`\n\n👆 Click To Copy", reply_markup=m.message.reply_markup)
    except Exception as e:
        print(e)
