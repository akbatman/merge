from dotenv import load_dotenv

load_dotenv(
    "config.env",
    override=True,
)
import asyncio
import os
import shutil
import time

import psutil
import pyromod
from PIL import Image
from pyrogram import Client, filters,enums
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    PeerIdInvalid,
    UserIsBlocked,
)
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    User,
)

from __init__ import (
    AUDIO_EXTENSIONS,
    BROADCAST_MSG,
    LOGGER,
    MERGE_MODE,
    SUBTITLE_EXTENSIONS,
    UPLOAD_AS_DOC,
    UPLOAD_TO_DRIVE,
    VIDEO_EXTENSIONS,
    bMaker,
    formatDB,
    gDict,
    queueDB,
    replyDB,
)
from config import Config
from helpers import database
from helpers.utils import UserSettings, get_readable_file_size, get_readable_time

botStartTime = time.time()
parent_id = Config.GDRIVE_FOLDER_ID


class MergeBot(Client):
    def start(self):
        super().start()
        try:
            self.send_message(chat_id=int(Config.LOGCHANNEL), text="<b>Robot has been Awaken Successfully 🥁</b>")
        except Exception as err:
            LOGGER.error("Boot Alert Failed! Please Start Bot In PM")
        return LOGGER.info("Robot has been Awaken Successfully 🥁")

    def stop(self):
        super().stop()
        return LOGGER.info("Bot Stopped 🚫")


mergeApp = MergeBot(
    name="merge-bot",
    api_hash=Config.API_HASH,
    api_id=Config.TELEGRAM_API,
    bot_token=Config.BOT_TOKEN,
    workers=300,
    plugins=dict(root="plugins"),
    app_version="5.0+yash-mergebot",
)


if os.path.exists("downloads") == False:
    os.makedirs("downloads")


@mergeApp.on_message(filters.command(["log"]) & filters.user(Config.OWNER_USERNAME))
async def sendLogFile(c: Client, m: Message):
    await m.reply_document(document="./mergebotlog.txt")
    return


@mergeApp.on_message(filters.command(["login"]) & filters.private)
async def loginHandler(c: Client, m: Message):
    user = UserSettings(m.from_user.id, m.from_user.first_name)
    if user.banned:
        await m.reply_text(text=f"**Banned User Detected!**\n  🛡️ Unfortunately You can't use me!!\n\nContact: @{Config.USERNAME}", quote=True)
        return
    if user.user_id == int(Config.OWNER):
        user.allowed = True
    if user.allowed:
        await m.reply_text(text=f"<b><i>😍 You Already have the 'Access' to use me!!</i></b>", quote=True)
    else:
        try:
            passwd = m.text.split(" ", 1)[1]
        except:
            await m.reply_text("**Command:**\n  `/login <password>`\n\n**Usage:**\n  `password`: Get the Password from my Owner!",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        passwd = passwd.strip()
        if passwd == Config.PASSWORD:
            user.allowed = True
            await m.reply_text(
                text=f"<b>✅ Access Granted!!,</b>\n <i>⚡ Now you can use my Powers!!</i>", quote=True
            )
        else:
            await m.reply_text(
                text=f"**❌ Login failed,**\n 🛡️ Unfortunately!!, you can't use me...\n\nContact: @{Config.USERNAME}",
                quote=True,
            )
    user.set()
    del user
    return


@mergeApp.on_message(filters.command(["stats"]) & filters.private)
async def stats_handler(c: Client, m: Message):
    currentTime = get_readable_time(time.time() - botStartTime)
    total, used, free = shutil.disk_usage(".")
    total = get_readable_file_size(total)
    used = get_readable_file_size(used)
    free = get_readable_file_size(free)
    sent = get_readable_file_size(psutil.net_io_counters().bytes_sent)
    recv = get_readable_file_size(psutil.net_io_counters().bytes_recv)
    cpuUsage = psutil.cpu_percent(interval=0.5)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = (
        f"<b>╭「  BOT STATISTICS 」</b>\n"
        f"<b>│</b>\n"
        f"<b>├⏳ Bot Uptime : {currentTime}</b>\n"
        f"<b>├ Total Disk Space : {total}</b>\n"
        f"<b>├ Total Used Space : {used}</b>\n"
        f"<b>├ Total Free Space : {free}</b>\n"
        f"<b>├ Total Upload : {sent}</b>\n"
        f"<b>├ Total Download : {recv}</b>\n"
        f"<b>├ CPU : {cpuUsage}%</b>\n"
        f"<b>├⚙️ RAM : {memory}%</b>\n"
        f"<b>╰ DISK : {disk}%</b>")  # Closed parenthesis

    markup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Close", callback_data="close")]
        ]
    )

    await m.reply_text(text=stats, reply_markup=markup, quote=True)



@mergeApp.on_message(
    filters.command(["broadcast"])
    & filters.private
    & filters.user(Config.OWNER_USERNAME)
)
async def broadcast_handler(c: Client, m: Message):
    msg = m.reply_to_message
    userList = await database.broadcast()
    len = userList.collection.count_documents({})
    status = await m.reply_text(text=BROADCAST_MSG.format(str(len), "0"), quote=True)
    success = 0
    for i in range(len):
        try:
            uid = userList[i]["_id"]
            if uid != int(Config.OWNER):
                await msg.copy(chat_id=uid)
            success = i + 1
            await status.edit_text(text=BROADCAST_MSG.format(len, success))
            LOGGER.info(f"Message sent to {userList[i]['name']} ")
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await msg.copy(chat_id=userList[i]["_id"])
            LOGGER.info(f"Message sent to {userList[i]['name']} ")
        except InputUserDeactivated:
            await database.deleteUser(userList[i]["_id"])
            LOGGER.info(f"{userList[i]['_id']} - {userList[i]['name']} : deactivated\n")
        except UserIsBlocked:
            await database.deleteUser(userList[i]["_id"])
            LOGGER.info(
                f"{userList[i]['_id']} - {userList[i]['name']} : blocked the bot\n"
            )
        except PeerIdInvalid:
            await database.deleteUser(userList[i]["_id"])
            LOGGER.info(
                f"{userList[i]['_id']} - {userList[i]['name']} : user id invalid\n"
            )
        except Exception as err:
            LOGGER.warning(f"{err}\n")
        await asyncio.sleep(3)
    await status.edit_text(
        text=BROADCAST_MSG.format(len, success)
        + f"**Failed: {str(len-success)}**\n\n__🛰️ Broadcast Completed Sucessfully!!__",
    )


@mergeApp.on_message(filters.command(["start"]) & filters.private)
async def start_handler(c: Client, m: Message):
    user = UserSettings(m.from_user.id, m.from_user.first_name)

    if m.from_user.id != int(Config.OWNER):
        if user.allowed is False:
            res = await m.reply_text(
                text=f"**Hello,** __{m.from_user.first_name}__\n\n 🛡️ Unfortunately!!, you can't use me...\n\n**Contact: @{Config.USERNAME}** ",
                quote=True,
            )
            return
    else:
        user.allowed = True
        user.set()
    res = await m.reply_text(
        text=f"<b>нєу</b> {m.from_user.first_name},\n\n<b>➻<i> I'm your file management guru! Merging videos, audio, and documents, and uploading them to Telegram & Drive is my superpower..</i></b>\n───────────────────\n<i>More details... /help</i> ",
        quote=True,
    )
    del user


@mergeApp.on_message(
    (filters.document | filters.video | filters.audio) & filters.private
)
async def files_handler(c: Client, m: Message):
    user_id = m.from_user.id
    user = UserSettings(user_id, m.from_user.first_name)
    if user_id != int(Config.OWNER):
        if user.allowed is False:
            res = await m.reply_text(
                text=f"**Hello,** __{m.from_user.first_name}__\n\n 🛡️ Unfortunately!!, you can't use me...\n\n**Contact: @{Config.USERNAME}** ",
                quote=True,
            )
            return
    if user.merge_mode == 4: # extract_mode
        return
    input_ = f"downloads/{str(user_id)}/input.txt"
    if os.path.exists(input_):
        await m.reply_text("nah nah 🥱,\nOne Process is already in System!\nWait for it to be Completed.")
        return
    media = m.video or m.document or m.audio
    if media.file_name is None:
        await m.reply_text("File Not Found")
        return
    currentFileNameExt = media.file_name.rsplit(sep=".")[-1].lower()
    if currentFileNameExt in "conf":
        await m.reply_text(
            text="**💾 Config File Found, Do You Want To Save It?**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("✅ Yes", callback_data=f"rclone_save"),
                        InlineKeyboardButton("❌ No", callback_data="rclone_discard"),
                    ]
                ]
            ),
            quote=True,
        )
        return
    # if MERGE_MODE.get(user_id) is None:
    #     userMergeMode = database.getUserMergeSettings(user_id)
    #     if userMergeMode is not None:
    #         MERGE_MODE[user_id] = userMergeMode
    #     else:
    #         database.setUserMergeMode(uid=user_id, mode=1)
    #         MERGE_MODE[user_id] = 1

    if user.merge_mode == 1:

        if queueDB.get(user_id, None) is None:
            formatDB.update({user_id: currentFileNameExt})
        if formatDB.get(
            user_id, None
        ) is not None and currentFileNameExt != formatDB.get(user_id):
            await m.reply_text(
                f"First you sent a {formatDB.get(user_id).upper()} file so now send only that type of file.",
                quote=True,
            )
            return
        if currentFileNameExt not in VIDEO_EXTENSIONS:
            await m.reply_text(
                "This Video Format Not Allowed!\nOnly send MP4 or MKV or WEBM.",
                quote=True,
            )
            return
        editable = await m.reply_text("🎗️", quote=True)
        MessageText = "<b>‣ To continue the merging process:</b>\n<i>- Add another video</i>\n<i>- Press </i><b>'🧬 Merge'</b> <i>Button to start merging the files.</i>"

        if queueDB.get(user_id, None) is None:
            queueDB.update({user_id: {"videos": [], "subtitles": [], "audios": []}})
        if (
            len(queueDB.get(user_id)["videos"]) >= 0
            and len(queueDB.get(user_id)["videos"]) < 20
        ):
            queueDB.get(user_id)["videos"].append(m.id)
            queueDB.get(m.from_user.id)["subtitles"].append(None)

            # LOGGER.info(
            #     queueDB.get(user_id)["videos"], queueDB.get(m.from_user.id)["subtitles"]
            # )

            if len(queueDB.get(user_id)["videos"]) == 1:
                reply_ = await editable.edit(
                    "<b><i>‣ Please send another 'Video' to continue the merging process.</i></b>",
                    reply_markup=InlineKeyboardMarkup(
                        bMaker.makebuttons(["Cancel"], ["cancel"])
                    ),
                )
                replyDB.update({user_id: reply_.id})
                return
            if queueDB.get(user_id, None)["videos"] is None:
                formatDB.update({user_id: currentFileNameExt})
            if replyDB.get(user_id, None) is not None:
                await c.delete_messages(
                    chat_id=m.chat.id, message_ids=replyDB.get(user_id)
                )
            if len(queueDB.get(user_id)["videos"]) == 20:
                MessageText = "Okay, Now Just Press <b>🧬 Merge** Button</b>"
            markup = await makeButtons(c, m, queueDB)
            reply_ = await editable.edit(
                text=MessageText, reply_markup=InlineKeyboardMarkup(markup)
            )
            replyDB.update({user_id: reply_.id})
        elif len(queueDB.get(user_id)["videos"]) > 20:
            markup = await makeButtons(c, m, queueDB)
            await editable.text(
                "Max 20 videos allowed", reply_markup=InlineKeyboardMarkup(markup)
            )

    elif user.merge_mode == 2:
        editable = await m.reply_text("💫", quote=True)
        MessageText = (
            "<b><u>‣ Please send another 'Audio' to continue the merging process.</u></b>"
        )

        if queueDB.get(user_id, None) is None:
            queueDB.update({user_id: {"videos": [], "subtitles": [], "audios": []}})
        if len(queueDB.get(user_id)["videos"]) == 0:
            queueDB.get(user_id)["videos"].append(m.id)
            # if len(queueDB.get(user_id)["videos"])==1:
            reply_ = await editable.edit(
                text="<i>Now, Send all the 'audios' you want to merge.</i>",
                reply_markup=InlineKeyboardMarkup(
                    bMaker.makebuttons(["Cancel"], ["cancel"])
                ),
            )
            replyDB.update({user_id: reply_.id})
            return
        elif (
            len(queueDB.get(user_id)["videos"]) >= 1
            and currentFileNameExt in AUDIO_EXTENSIONS
        ):
            queueDB.get(user_id)["audios"].append(m.id)
            if replyDB.get(user_id, None) is not None:
                await c.delete_messages(
                    chat_id=m.chat.id, message_ids=replyDB.get(user_id)
                )
            markup = await makeButtons(c, m, queueDB)

            reply_ = await editable.edit(
                text=MessageText, reply_markup=InlineKeyboardMarkup(markup)
            )
            replyDB.update({user_id: reply_.id})
        else:
            await m.reply("This Filetype is not valid")
            return

    elif user.merge_mode == 3:

        editable = await m.reply_text("💫", quote=True)
        MessageText = "<b><u>‣ Please send another 'Subtitle' to continue the merging process.</u></b>"
        if queueDB.get(user_id, None) is None:
            queueDB.update({user_id: {"videos": [], "subtitles": [], "audios": []}})
        if len(queueDB.get(user_id)["videos"]) == 0:
            queueDB.get(user_id)["videos"].append(m.id)
            # if len(queueDB.get(user_id)["videos"])==1:
            reply_ = await editable.edit(
                text="<i>Now, Send All The 'Subtitles' You Want To Merge.<i>",
                reply_markup=InlineKeyboardMarkup(
                    bMaker.makebuttons(["Cancel"], ["cancel"])
                ),
            )
            replyDB.update({user_id: reply_.id})
            return
        elif (
            len(queueDB.get(user_id)["videos"]) >= 1
            and currentFileNameExt in SUBTITLE_EXTENSIONS
        ):
            queueDB.get(user_id)["subtitles"].append(m.id)
            if replyDB.get(user_id, None) is not None:
                await c.delete_messages(
                    chat_id=m.chat.id, message_ids=replyDB.get(user_id)
                )
            markup = await makeButtons(c, m, queueDB)

            reply_ = await editable.edit(
                text=MessageText, reply_markup=InlineKeyboardMarkup(markup)
            )
            replyDB.update({user_id: reply_.id})
        else:
            await m.reply("This Filetype is not valid")
            return


@mergeApp.on_message(filters.photo & filters.private)
async def photo_handler(c: Client, m: Message):
    user = UserSettings(m.chat.id, m.from_user.first_name)
    # if m.from_user.id != int(Config.OWNER):
    if not user.allowed:
        res = await m.reply_text(
            text=f"Hi **{m.from_user.first_name}**\n\n 🛡️ Unfortunately!!, you can't use me...\n\n**Contact: @{Config.USERNAME}** ",
            quote=True,
        )
        del user
        return
    thumbnail = m.photo.file_id
    msg = await m.reply_text("<i>Saving Thumbnail. . . .</i>", quote=True)
    user.thumbnail = thumbnail
    user.set()
    # await database.saveThumb(m.from_user.id, thumbnail)
    LOCATION = f"downloads/{m.from_user.id}_thumb.jpg"
    await c.download_media(message=m, file_name=LOCATION)
    await msg.edit_text(text="<i>✅ Custom Thumbnail Saved!</i>")
    del user


@mergeApp.on_message(filters.command(["extract"]) & filters.private)
async def media_extracter(c: Client, m: Message):
    user = UserSettings(uid=m.from_user.id, name=m.from_user.first_name)
    if not user.allowed:
        return
    if user.merge_mode == 4:
        if m.reply_to_message is None:
            await m.reply(text="Reply /extract to a video or document file")
            return
        rmess = m.reply_to_message
        if rmess.video or rmess.document:
            media = rmess.video or rmess.document
            mid=rmess.id
            file_name = media.file_name
            if file_name is None:
                await m.reply("File name not found: goto Support!")
                return
            markup = bMaker.makebuttons(
                set1=["Audio", "Subtitle", "Cancel"],
                set2=[f"extract_audio_{mid}", f"extract_subtitle_{mid}", 'cancel'],
                isCallback=True,
                rows=2,
            )
            await m.reply(
                text="Choose from below what you want to extract?",
                quote=True,
                reply_markup=InlineKeyboardMarkup(markup),
            )
    else:
        await m.reply(
            text="Change settings and set mode to extract\nthen use /extract command"
        )


@mergeApp.on_message(filters.command(["help"]) & filters.private)
async def help_msg(c: Client, m: Message):
    await m.reply_text(
        text="""ㄖ <b><u>Follow These STEPS</u> :</b>
- - - - - - - - - - - - - - - - - - - - - - - - - - -
<b>• Send me the custom thumbnail</b> <i>(optional)</i>
<b>• Send two or more Your Videos Which you want to merge.</b>
<b>• After sending all files select merge options.</b>
<b>• Select the upload mode.</b>
<b>• Select rename if you want to give custom file name else press default.</b>
───────────────────
<i>Change your setting from /settings</i>""",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Close", callback_data="close")]]
        ),
    )


@mergeApp.on_message(filters.command(["about"]) & filters.private)
async def about_handler(c: Client, m: Message):
    await m.reply_text(
        text="""<b>❪ <u>About this Bot</u> ❫</b>
- - - - - - - - - - - - - - - - - - - - - - - - - - -
<b>• Custom Thumbnails</b>
<b>• Preserves Metadata</b>
<b>• Access through Passcode</b>
<b>• Direct Drive Upload</b> <i>(Config)</i>
<b>• Extract Audio/Subtitles from File</b>
<b>• Merge Up to 20</b> <i>(Video/Audio/Docs)</i>
<b>• Upload as Document or Video Format</b>
───────────────────
<i>Check Bot Stats /stats</i>
                    """,
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("• Channel •", url="https://t.me/Anaavaran"),
                InlineKeyboardButton("• Owner •", url="https://t.me/itsmeflashh")
                   ],[ 
	       InlineKeyboardButton("Close", callback_data="close")],
            ]
        ),
    )


@mergeApp.on_message(
    filters.command(["savethumb", "setthumb", "savethumbnail"]) & filters.private
)
async def save_thumbnail(c: Client, m: Message):
    if m.reply_to_message:
        if m.reply_to_message.photo:
            await photo_handler(c, m.reply_to_message)
        else:
            await m.reply(text="Please reply to a valid photo")
    else:
        await m.reply(text="Please reply to a message")
    return


@mergeApp.on_message(filters.command(["showthumbnail"]) & filters.private)
async def show_thumbnail(c: Client, m: Message):
    try:
        user = UserSettings(m.from_user.id, m.from_user.first_name)
        thumb_id = user.thumbnail
        LOCATION = f"downloads/{str(m.from_user.id)}_thumb.jpg"
        if os.path.exists(LOCATION):
            await m.reply_photo(
                photo=LOCATION, caption="🖼️ Your Custom Thumbnail", quote=True
            )
        elif thumb_id is not None :
            await c.download_media(message=str(thumb_id), file_name=LOCATION)
            await m.reply_photo(
                photo=LOCATION, caption="🖼️ Your Custom Thumbnail", quote=True
            )
        else: 
            await m.reply_text(text="❌ Custom Thumbnail Not Found", quote=True)
        del user
    except Exception as err:
        LOGGER.info(err)
        await m.reply_text(text="❌ Custom Thumbnail Not Found", quote=True)


@mergeApp.on_message(filters.command(["deletethumbnail"]) & filters.private)
async def delete_thumbnail(c: Client, m: Message):
    try:
        user = UserSettings(m.from_user.id, m.from_user.first_name)
        user.thumbnail = None
        user.set()
        if os.path.exists(f"downloads/{str(m.from_user.id)}"):
            os.remove(f"downloads/{str(m.from_user.id)}")
            await m.reply_text("✅ Deleted Sucessfully", quote=True)
            del user
        else: raise Exception("Thumbnail File Not Found")
    except Exception as err:
        await m.reply_text(text="❌ Custom Thumbnail Not Found", quote=True)

@mergeApp.on_message(filters.command(["ban","unban"]) & filters.private)
async def ban_user(c:Client,m:Message):
    incoming=m.text.split(' ')[0]
    if incoming == '/ban':
        if m.from_user.id == int(Config.OWNER):
            try:
                abuser_id = int(m.text.split(" ")[1])
                if abuser_id == int(Config.OWNER):
                    await m.reply_text("I can't ban you master,\nPlease don't abandon me. ",quote=True)
                else:
                    try:
                        user_obj: User = await c.get_users(abuser_id)
                        udata  = UserSettings(uid=abuser_id,name=user_obj.first_name)
                        udata.banned=True
                        udata.allowed=False
                        udata.set()
                        await m.reply_text(f"Pooof, {user_obj.first_name} has been **BANNED**",quote=True)
                        acknowledgement = f"""
Dear {user_obj.first_name},
I found your messages annoying and forwarded them to our team of moderators for inspection. The moderators have confirmed the report and your account is now banned.

While the account is banned, you will not be able to do certain things, like merging videos/audios/subtitles or extract audios from Telegram media.

Your Account Can Be Released Only By @{Config.USERNAME}."""
                        try:
                            await c.send_message(
                                chat_id=abuser_id,
                                text=acknowledgement
                            )
                        except Exception as e:
                            await m.reply_text(f"An Error Occured While Sending Acknowledgement\n\n`{e}`",quote=True)
                            LOGGER.error(e)
                    except Exception as e:
                        LOGGER.error(e)
            except:
                await m.reply_text("**Command:**\n  `/ban <user_id>`\n\n**Usage:**\n  `user_id`: User ID of the user",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        else:
            await m.reply_text("**(Only for __OWNER__)\nCommand:**\n  `/ban <user_id>`\n\n**Usage:**\n  `user_id`: User ID of the user",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        return
    elif incoming == '/unban':
        if m.from_user.id == int(Config.OWNER):
            try:
                abuser_id = int(m.text.split(" ")[1])
                if abuser_id == int(Config.OWNER):
                    await m.reply_text("I Can't Ban You Master,\nPlease Don't Abandon Me. ",quote=True)
                else:
                    try:
                        user_obj: User = await c.get_users(abuser_id)
                        udata  = UserSettings(uid=abuser_id,name=user_obj.first_name)
                        udata.banned=False
                        udata.allowed=True
                        udata.set()
                        await m.reply_text(f"Pooof, {user_obj.first_name} has been **UN_BANNED**",quote=True)
                        release_notice = f"""
Good News {user_obj.first_name}, The Ban Has Been Uplifted On Your Account. You're Free As A Bird!"""
                        try:
                            await c.send_message(
                                chat_id=abuser_id,
                                text=release_notice
                            )
                        except Exception as e:
                            await m.reply_text(f"An Error Occured While Sending Release Notice\n\n`{e}`",quote=True)
                            LOGGER.error(e)                      
                    except Exception as e:
                        LOGGER.error(e)
            except:
                await m.reply_text("**Command:**\n  `/unban <user_id>`\n\n**Usage:**\n  `user_id`: User ID of the user",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        else:
            await m.reply_text("**(Only for __OWNER__)\nCommand:**\n  `/unban <user_id>`\n\n**Usage:**\n  `user_id`: User ID of the user",quote=True,parse_mode=enums.parse_mode.ParseMode.MARKDOWN)
        return
async def showQueue(c: Client, cb: CallbackQuery):
    try:
        markup = await makeButtons(c, cb.message, queueDB)
        await cb.message.edit(
            text="Okay,\nNow send me Another File or Press <b>🧬 Merge</b> Button!",
            reply_markup=InlineKeyboardMarkup(markup),
        )
    except ValueError:
        await cb.message.edit("Send me, some more Files.")
    return


async def delete_all(root):
    try:
        shutil.rmtree(root)
    except Exception as e:
        LOGGER.info(e)


async def makeButtons(bot: Client, m: Message, db: dict):
    markup = []
    user = UserSettings(m.chat.id, m.chat.first_name)
    if user.merge_mode == 1:
        for i in await bot.get_messages(
            chat_id=m.chat.id, message_ids=db.get(m.chat.id)["videos"]
        ):
            media = i.video or i.document or None
            if media is None:
                continue
            else:
                markup.append(
                    [
                        InlineKeyboardButton(
                            f"{media.file_name}",
                            callback_data=f"showFileName_{i.id}",
                        )
                    ]
                )

    elif user.merge_mode == 2:
        msgs: list[Message] = await bot.get_messages(
            chat_id=m.chat.id, message_ids=db.get(m.chat.id)["audios"]
        )
        msgs.insert(
            0,
            await bot.get_messages(
                chat_id=m.chat.id, message_ids=db.get(m.chat.id)["videos"][0]
            ),
        )
        for i in msgs:
            media = i.audio or i.document or i.video or None
            if media is None:
                continue
            else:
                markup.append(
                    [
                        InlineKeyboardButton(
                            f"{media.file_name}",
                            callback_data=f"tryotherbutton",
                        )
                    ]
                )

    elif user.merge_mode == 3:
        msgs: list[Message] = await bot.get_messages(
            chat_id=m.chat.id, message_ids=db.get(m.chat.id)["subtitles"]
        )
        msgs.insert(
            0,
            await bot.get_messages(
                chat_id=m.chat.id, message_ids=db.get(m.chat.id)["videos"][0]
            ),
        )
        for i in msgs:
            media = i.video or i.document or None

            if media is None:
                continue
            else:
                markup.append(
                    [
                        InlineKeyboardButton(
                            f"{media.file_name}",
                            callback_data=f"tryotherbutton",
                        )
                    ]
                )

    markup.append([InlineKeyboardButton("╰┈► 🧬 Merge ◄┈╯", callback_data="merge")])
    markup.append([InlineKeyboardButton("🗑️ Clear the List", callback_data="cancel")])
    return markup


LOGCHANNEL = Config.LOGCHANNEL
try:
    if Config.USER_SESSION_STRING is None:
        raise KeyError
    LOGGER.info("Starting USER Session")
    userBot = Client(
        name="merge-bot-user",
        session_string=Config.USER_SESSION_STRING,
        no_updates=True,
    )

except KeyError:
    userBot = None
    LOGGER.warning("No User Session, Default Bot session will be used")


if __name__ == "__main__":
    # with mergeApp:
    #     bot:User = mergeApp.get_me()
    #     bot_username = bot.username
    try:
        with userBot:
            userBot.send_message(
                chat_id=int(LOGCHANNEL),
                text="Bot Booted With Premium Account 🌟,\n\n  Thanks For Using <a href='https://t.me/Anaavaran'>using my Services</a>",
                disable_web_page_preview=True,
            )
            user = userBot.get_me()
            Config.IS_PREMIUM = user.is_premium
    except Exception as err:
        LOGGER.error(f"{err}")
        Config.IS_PREMIUM = False
        pass

    mergeApp.run()
