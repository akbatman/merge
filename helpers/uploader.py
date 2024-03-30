import asyncio
import os
import time

from __init__ import LOGGER
from bot import LOGCHANNEL, userBot
from config import Config
from pyrogram import Client
from pyrogram.types import CallbackQuery, Message

from helpers.display_progress import Progress


async def uploadVideo(
    c: Client,
    cb: CallbackQuery,
    merged_video_path,
    width,
    height,
    duration,
    video_thumbnail,
    file_size,
    upload_mode: bool,
):
    # Report your errors in telegram group (@yo_codes).
    if Config.IS_PREMIUM:
        sent_ = None
        file_count = 0  # Initialize file count variable

        # Count files in the directory containing video parts
        for filename in os.listdir(os.path.dirname(merged_video_path)):
            if os.path.isfile(os.path.join(os.path.dirname(merged_video_path), filename)):
                file_count += 1

        prog = Progress(cb.from_user.id, c, cb.message)
        async with userBot:
            if upload_mode is False:
                c_time = time.time()
                sent_: Message = await userBot.send_video(
                    chat_id=int(LOGCHANNEL),
                    video=merged_video_path,
                    height=height,
                    width=width,
                    duration=duration,
                    thumb=video_thumbnail,
                    caption=f"`{merged_video_path.rsplit('/', 1)[-1]}`\n\nMerged using {file_count} files\n\nMerged by: {cb.from_user.mention}",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"Uploading: `{merged_video_path.rsplit('/', 1)[-1]}`",
                        c_time,
                    ),
                )
                # ... rest of your code within the if block ...
            else:
                # ... similar logic for upload_mode True ...

    else:
        # ... rest of your code for non-premium users ...


async def uploadFiles(
    c: Client,
    cb: CallbackQuery,
    up_path,
    n,
    all
):
    try:
        sent_ = None
        prog = Progress(cb.from_user.id, c, cb.message)
        c_time = time.time()
        sent_: Message = await c.send_document(
            chat_id=cb.message.chat.id,
            document=up_path,
            caption=f"`{up_path.rsplit('/', 1)[-1]}`\n\n**Uploading: {n}/{all}**",
            progress=prog.progress_for_pyrogram,
            progress_args=(
                f"Uploading: `{up_path.rsplit('/', 1)[-1]}`",
                c_time,
            ),
        )
        if sent_ is not None:
            if Config.LOGCHANNEL is not None:
                media = sent_.video or sent_.document
                await sent_.copy(
                    chat_id=int(LOGCHANNEL),
                    caption=f"`{media.file_name}`\n\nExtracted by: <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>",
                )
    except:
        pass


# ... rest of your code ...
