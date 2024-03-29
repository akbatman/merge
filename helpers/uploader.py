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
                    caption=f"╭ <i>{merged_video_path.rsplit('/',1)[-1]}</i>\n│\n • <i>total files: {all}</i>\n│\n╰─┈ <b>user:</b> {cb.from_user.mention}",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"<b>〘  Uploading to Telegram 〙</b>\n\n<b> Name: </b><i>{merged_video_path.rsplit('/',1)[-1]}</i>",
                        c_time,
                    ),
                )
            else:
                c_time = time.time()
                sent_: Message = await userBot.send_document(
                    chat_id=int(LOGCHANNEL),
                    document=merged_video_path,
                    thumb=video_thumbnail,
                    caption=f"╭ <i>{merged_video_path.rsplit('/',1)[-1]}</i>\n│\n • <i>total files: {all}</i>\n│\n╰─┈ <b>user:</b> <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a>",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"<b>〘  Uploading to Telegram 〙</b>\n\n<b> Name: </b><i>{merged_video_path.rsplit('/',1)[-1]}</i>",
                        c_time,
                    ),
                )
            if sent_ is not None:
                # Integration point: Modify the caption and handle copying the message (optional)
                caption = f"<b>{merged_video_path.rsplit('/', 1)[-1]}</b>\n\n • Total Files: {all}"  # Assuming 'all' represents the total files

                # Optional: Copy the uploaded message to the user's chat
                await c.copy_message(
                    chat_id=cb.message.chat.id,
                    from_chat_id=sent_.chat.id,
                    message_id=sent_.id,
                    caption=caption,
                )
                # await sent_.delete()
    else:
        try:
            sent_ = None
            prog = Progress(cb.from_user.id, c, cb.message)
            if upload_mode is False:
                c_time = time.time()
                sent_: Message = await c.send_video(
                    chat_id=cb.message.chat.id,
                    video=merged_video_path,
                    height=height,
                    width=width,
                    duration=duration,
                    thumb=video_thumbnail,
                    caption=f"<b>{merged_video_path.rsplit('/',1)[-1]}</b>",
                    progress=prog.progress_for_pyrogram,
                    progress_args=(
                        f"<b>〘  Uploading to Telegram 〙</b>\n\n<b> Name: </b><i>{merged_video_path.rsplit('/',1)[-1]}</i>",
                        c_time,
                    ),
                )
            else:
                c_time = time.time()
                sent_: Message = await c.send_document(
                    chat_id=cb.message.chat.id,
                    document=merged_video_path,

                
