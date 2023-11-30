from pyrogram import Client, filters, enums
from info import COMMAND_HAND_LER
from plugins.helper_functions.cust_p_filters import f_onw_fliter

# LUCK------------ https://telegram.me/NobiDeveloper ------------ #

# EMOJI CONSTANTS
TRY_YOUR_LUCK = "🎰"
# EMOJI CONSTANTS

@Client.on_message(
    filters.command(["luck", "cownd"])
)
async def luck_cownd(client, message):
    """ /luck an @animatedluck """
    rep_mesg_id = message.id
    if message.reply_to_message:
        rep_mesg_id = message.reply_to_message.id
    await client.send_dice(
        chat_id=message.chat.id,
        emoji=TRY_YOUR_LUCK,
        disable_notification=True,
        reply_to_message_id=rep_mesg_id
    )