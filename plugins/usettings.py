import time
from pyrogram import filters, Client as mergeApp
from pyrogram.types import Message, InlineKeyboardMarkup
from helpers.msg_utils import MakeButtons
from helpers.utils import UserSettings


@mergeApp.on_message(filters.command(["settings"]))
async def f1(c: mergeApp, m: Message):
    # setUserMergeMode(uid=m.from_user.id,mode=1)
    replay = await m.reply(text="Please wait", quote=True)
    usettings = UserSettings(m.from_user.id, m.from_user.first_name)
    await userSettings(
        replay, m.from_user.id, m.from_user.first_name, m.from_user.last_name, usettings
    )


async def userSettings(
    editable: Message,
    uid: int,
    fname,
    lname,
    usettings: UserSettings,
):
    b = MakeButtons()
    if usettings.user_id:
        if usettings.merge_mode == 1:
            userMergeModeId = 1
            userMergeModeStr = "🖼️ Video + 🖼️ Video"
        elif usettings.merge_mode == 2:
            userMergeModeId = 2
            userMergeModeStr = "🖼️ Video + 🔊 Audio"
        elif usettings.merge_mode == 3:
            userMergeModeId = 3
            userMergeModeStr = "🖼️ Video + 📜 Subtitle"
        elif usettings.merge_mode == 4:
            userMergeModeId = 4
            userMergeModeStr = "🗜️ Extract" 
        if usettings.edit_metadata:
            editMetadataStr = "✅"
        else:
            editMetadataStr = "❌"
        uSettingsMessage = f"""
<b><u>❰ User Specific Merge Settings ❱</u></b>
    ┃
    ┣ <b>🪪 ID:</b> <i>{usettings.user_id}</i>
    ┣ {'🚫' if usettings.banned else '🫡'} <b>Ban Status:</b> <i>{usettings.banned}</i>
    ┣ {'⚡' if usettings.allowed else '❗'} <b>Allowed:</b> <i>{usettings.allowed}</i>
    ┣ {'✅' if usettings.edit_metadata else '❌'} <b>Edit Metadata:</b> <i>{usettings.edit_metadata}</i>
    ┗ <b>Ⓜ️ Merge mode:</b> <i>{userMergeModeStr}</i>
"""
        markup = b.makebuttons(
            [
                "Merge mode",
                userMergeModeStr,
                "Edit Metadata",
                editMetadataStr,
                "Close",
            ],
            [
                "tryotherbutton",
                f"ch@ng3M0de_{uid}_{(userMergeModeId%4)+1}",
                "tryotherbutton",
                f"toggleEdit_{uid}",
                "close",
            ],
            rows=2,
        )
        res = await editable.edit(
            text=uSettingsMessage, reply_markup=InlineKeyboardMarkup(markup)
        )
    else:
        usettings.name = fname
        usettings.merge_mode = 1
        usettings.allowed = False
        usettings.edit_metadata = False
        usettings.thumbnail = None
        await userSettings(editable, uid, fname, lname, usettings)
    # await asyncio.sleep(10)
    # await c.delete_messages(chat_id=editable.chat.id, message_ids=[res.id-1,res.id])
    return
