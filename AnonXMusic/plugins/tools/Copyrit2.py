import os
import logging
from pyrogram import filters
from AnonXMusic import pbot as app
from pyrogram.types import User

# -------------------------------

def time_formatter(milliseconds: float) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def size_formatter(bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            break
        bytes /= 1024.0
    return f"{bytes:.2f} {unit}"

# -----------------------------------------------------------

FORBIDDEN_KEYWORDS = ["porn", "xxx", "sex", "NCERT", "XII", "page", "Ans", "meiotic", "divisions", "System.in", "Scanner", "void", "nextInt"]

@app.on_message(filters.private)
async def handle_message(client, message):
    if any(keyword in message.text for keyword in FORBIDDEN_KEYWORDS):
        logging.info(f"✦ ᴅᴇʟᴇᴛɪɴɢ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ɪᴅ {message.message_id}")
        await message.delete()
        user_mention = message.from_user.mention
        await message.reply_text(f"✦ ʜᴇʏ {user_mention}, ʙᴀʙʏ ᴅᴏɴ'ᴛ sᴇɴᴅ ɴᴇxᴛ ᴛɪᴍᴇ.")
    if message.caption and any(keyword in message.caption for keyword in FORBIDDEN_KEYWORDS):
        logging.info(f"✦ ᴅᴇʟᴇᴛɪɴɢ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ ɪᴅ {message.message_id}")
        await message.delete()
        user_mention = message.from_user.mention
        await message.reply_text(f"✦ ʜᴇʏ {user_mention}, ʙᴀʙʏ ᴅᴏɴ'ᴛ sᴇɴᴅ, ɴᴇxᴛ ᴛɪᴍᴇ.")

# -----------------------------------------------------------
@app.on_edited_message(filters.group & ~filters.me)
async def delete_edited_messages(client, edited_message):
    await edited_message.delete()

# ------------------------------------------------------------
def delete_long_messages(_, m):
    return len(m.text.split()) > 400

@app.on_message(filters.group & filters.private & delete_long_messages)
async def delete_and_reply(_, msg):
    await msg.delete()
    user_mention = msg.from_user.mention
    await app.send_message(msg.chat.id, f"✦ ʜᴇʏ {user_mention} ʙᴀʙʏ, ᴘʟᴇᴀsᴇ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ sʜᴏʀᴛ.")
     #-----------------------------------------------------------

async def delete_pdf_files(client, message):
    if message.document and message.document.mime_type == "application/pdf":
        warning_message = f"✦ ʜᴇʏ {message.from_user.mention} ᴅᴏɴ'ᴛ sᴇɴᴅ ᴘᴅғ ғɪʟᴇs ʙᴀʙʏ, ғᴏʀ ᴄᴏᴘʏʀɪɢʜᴛ ᴄʟɪᴍʙ."
        await message.reply_text(warning_message)
        await message.delete()
    else:  
        pass

@app.on_message(filters.group & filters.document)
async def message_handler(client, message):
    await delete_pdf_files(client, message)
