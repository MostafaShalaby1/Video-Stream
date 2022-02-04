from datetime import datetime
from sys import version_info
from time import time

from config import (
    ALIVE_IMG,
    ALIVE_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from program import __version__
from driver.veez import user
from driver.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram import __version__ as pyrover
from pytgcalls import (__version__ as pytover)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

__major__ = 0
__minor__ = 2
__micro__ = 1

__python_version__ = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"


START_TIME = datetime.utcnow()
START_TIME_ISO = START_TIME.replace(microsecond=0).isoformat()
TIME_DURATION_UNITS = (
    ("week", 60 * 60 * 24 * 7),
    ("day", 60 * 60 * 24),
    ("hour", 60 * 60),
    ("min", 60),
    ("sec", 1),
)


async def _human_time_duration(seconds):
    if seconds == 0:
        return "inf"
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append("{} {}{}".format(amount, unit, "" if amount == 1 else "s"))
    return ", ".join(parts)


@Client.on_message(
    command(["start", f"start@{BOT_USERNAME}"]) & filters.private & ~filters.edited
)
async def start_(client: Client, message: Message):
    await message.reply_text(
        f"""✨ **مرحبا بيك {message.from_user.mention()} !**\n
💭 [{BOT_NAME}](https://t.me/{BOT_USERNAME}) **يتيح لك تشغيل الموسيقى والفيديو في مجموعات من خلال محادثات الفيديو الجديدة في Telegram!**

💡 **اكتشف جميع أوامر الروبوت وكيفية عملها من خلال النقر فوق » 📚 زر الاوامر!**

🔖 **لمعرفة كيفية استخدام هذا الروبوت ، الرجاء النقر فوق » ❓ زر الدليل الاساسي!**
""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "اضـف الـبـوت لـ مـجـمـوعـتـك 💥",
                        url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    )
                ],
                [InlineKeyboardButton("❓ زر الدليل الاساسي", callback_data="cbhowtouse")],
                [
                    InlineKeyboardButton("📚 الاوامر", callback_data="cbcmds"),
                    InlineKeyboardButton("❤️ مطور البوت", url=f"https://t.me/{OWNER_NAME}"),
                ],
                [
                    InlineKeyboardButton(
                        "👥 البشمبرمج عـازف", url=f"https://t.me/X_X_A_Z_F_X_X"
                    ),
                    InlineKeyboardButton(
                        "📣 قناة البوت", url=f"https://t.me/{UPDATES_CHANNEL}"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        "🌐 البشمبرمج سـافو", url="https://t.me/s_a_s_a_3li"
                    )
                ],
            ]
        ),
        disable_web_page_preview=True,
    )


@Client.on_message(
    command(["alive", f"alive@{BOT_USERNAME}", "سورس"]) & filters.group & ~filters.edited
)
async def alive(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("✨ البشمبرمج سـافو", url=f"https://t.me/s_a_s_a_3li"),
                InlineKeyboardButton(
                    "📣 قناة السورس", url=f"https://t.me/L_S_A_V_O"
                ),
            ]
        ]
    )

    alive = f"**مرحبا {message.from_user.mention()}, i m {BOT_NAME}**\n\n✨ يعمل البوت بشكل طبيعي\n🍀 سيدي: [{ALIVE_NAME}](https://t.me/{OWNER_NAME})\n✨ نسخة البوت: `v{__version__}`\n🍀 نسخة بيروجرام: `{pyrover}`\n✨ نسخة بايثون: `{__python_version__}`\n🍀 فيثاغورس والترخيص: `{pytover.__version__}`\n✨ حالة الجهوزية: `{uptime}`\n\n**شكرا لإضافتي هنا ، لتشغيل الفيديو & الموسيقى في دردشة الفيديو الجماعية الخاصة بك** ❤"

    await message.reply_photo(
        photo=f"{ALIVE_IMG}",
        caption=alive,
        reply_markup=keyboard,
    )


@Client.on_message(command(["ping", f"ping@{BOT_USERNAME}", "بينج"]) & ~filters.edited)
async def ping_pong(client: Client, message: Message):
    start = time()
    m_reply = await message.reply_text("pinging...")
    delta_ping = time() - start
    await m_reply.edit_text("🏓 `البينج مظبوط يسـافو`\n" f"⚡️ `{delta_ping * 1000:.3f} ms`")


@Client.on_message(command(["uptime", f"uptime@{BOT_USERNAME}", "بوت"]) & ~filters.edited)
async def get_uptime(client: Client, message: Message):
    current_time = datetime.utcnow()
    uptime_sec = (current_time - START_TIME).total_seconds()
    uptime = await _human_time_duration(int(uptime_sec))
    await message.reply_text(
        "🤖 حالة البوت:\n"
        f"• **الجهوزية:** `{uptime}`\n"
        f"• **وقت البدء:** `{START_TIME_ISO}`"
    )


@Client.on_message(filters.new_chat_members)
async def new_chat(c: Client, m: Message):
    ass_uname = (await user.get_me()).username
    bot_id = (await c.get_me()).id
    for member in m.new_chat_members:
        if member.id == bot_id:
            return await m.reply(
                "❤️ **شكرا لإضافتي إلى المجموعة !**\n\n"
                "**قم بترقيتي كمسؤول عن المجموعة ، وإلا فلن أتمكن من العمل بشكل صحيح ، ولا تنسى الكتابة /userbotjoin لدعوة المساعد.**\n\n"
                "**Once done, type** /reload",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("📣 قناة السورس", url=f"https://t.me/L_S_A_V_O"),
                            InlineKeyboardButton("💭 البشمبرمج سـافو", url=f"https://t.me/s_a_s_a_3li")
                        ],
                        [
                            InlineKeyboardButton("👤 حساب المساعد", url=f"https://t.me/{ass_uname}")
                        ]
                    ]
                )
            )

