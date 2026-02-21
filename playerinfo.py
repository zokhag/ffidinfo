import aiohttp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = "8290274056:AAETZl83qainaVWfmQTHS_H9pZnTkxB2WgQ"
ADMIN_ID = 7116845457  # your Telegram numeric ID

REQUIRED_CHANNELS = [-1002307015739, -1003489577704, -1003277917217]
CHANNEL_LINKS = [
    "https://t.me/+DdjfUVBQ2zE0MTI1",
    "https://t.me/+db2pmZ6HoIs2YWE1",
    "https://t.me/+w3C_dWmpQcwwZDE1",
]
INSTAGRAM_LINK = "https://instagram.com/yourpage"
API_URL = "https://abbas-apis.vercel.app/api/ff-info?uid="

WELCOME_ANIMATION = "https://media.giphy.com/media/3o7aD2saalBwwftBIY/giphy.gif"

USERS = set()
MAINTENANCE = False


# ---------- UTIL ----------
async def is_user_joined(context, user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(channel, user_id)
            if member.status not in ("member", "administrator", "creator"):
                return False
        except:
            return False
    return True


def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔍 SEARCH PLAYER INFO", callback_data="info")],
        [InlineKeyboardButton("💎 PAID GLORY PUSH", callback_data="paid_glory")]
    ])


# ---------- START ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    USERS.add(user_id)

    if MAINTENANCE and user_id != ADMIN_ID:
        await update.message.reply_text("🛠 Bot is under maintenance.")
        return

    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "👑 Admin Access Granted\n\nSend UID anytime to search.",
            reply_markup=main_keyboard()
        )
        return

    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url=CHANNEL_LINKS[0])],
        [InlineKeyboardButton("📢 Join Channel 2", url=CHANNEL_LINKS[1])],
        [InlineKeyboardButton("📢 Join Channel 3", url=CHANNEL_LINKS[2])],
        [InlineKeyboardButton("📸 Instagram", url=INSTAGRAM_LINK)],
        [InlineKeyboardButton("✅ I've Joined", callback_data="check_join")],
    ]

    await update.message.reply_animation(
        animation=WELCOME_ANIMATION,
        caption=(
            "🎃 WELCOME TO GLORY SERVICE BOT 🎃\n\n"
            "👉 Join all 3 private channels\n"
            "👉 Click I've Joined\n\n"
            "👨‍💻 Developer: @kaddu_yt9"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ---------- JOIN CHECK ----------
async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if await is_user_joined(context, query.from_user.id):
        await query.message.reply_text(
            "✅ Access granted!\n\nSend UID anytime to search.",
            reply_markup=main_keyboard()
        )
    else:
        await query.message.reply_text("❌ Join ALL channels first!")


# ---------- BUTTON INFO ----------
async def info_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "🔍 SEARCH PLAYER INFO\n\n"
        "Send Free Fire UID (numbers only)\n\n"
        "Example:\n11865167459"
    )


# ---------- PAID GLORY ----------
async def paid_glory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.message.reply_text(
        "💎 PAID GLORY PUSH 💎\n\n"
        "✔ Fast delivery\n"
        "✔ Safe & secure\n"
        "✔ Trusted service\n\n"
        "PRICE LIST:\n"
        "• 50K+ Glory – ₹210\n"
        "• 100K+ Glory – ₹350\n"
        "• 150K+ Glory – ₹500\n"
        "• 300K+ Glory – ₹900\n"
        "• 500K+ Glory – ₹1500\n\n"
        "📩 dm @iamnotsanju\n"
        "👨‍💻 Developer: @kaddu_yt9"
    )


# ---------- TEXT HANDLER (AUTO UID) ----------
async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if MAINTENANCE and user_id != ADMIN_ID:
        return

    # Ignore non-numeric messages
    if not text.isdigit():
        return

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}{text}", timeout=15) as resp:
                data = await resp.json()

        if not data.get("success"):
            await update.message.reply_text("❌ Player not found.")
            return

        info = data["data"]

        result = (
            "🎮 PLAYER INFORMATION 🎮\n\n"
            f"👤 Nickname: {info.get('👤 Nickname','N/A')}\n"
            f"🆔 UID: {info.get('🆔 ID',text)}\n"
            f"🌎 Region: {info.get('🌍 Region','N/A')}\n"
            f"🎖️ Level: {info.get('🎖️ Level','N/A')}\n"
            f"🏆 Ranked Points: {info.get('🏆 Ranked Points','N/A')}\n"
            f"👍 Likes: {info.get('👍 Likes','N/A')}\n"
            f"📈 XP: {info.get('📈 Experience (XP)','N/A')}\n"
            f"📅 Created: {info.get('📅 Account Created','N/A')}\n"
            f"🕒 Last Login: {info.get('🕒 Last Login','N/A')}\n"
            f"📝 Bio: {info.get('📝 Signature – Bio','N/A')}\n"
            f"🥇 Prime: {info.get('🥇 Prime','N/A')}\n\n"
            "📢 Channel: @kaddu_yt9\n"
            "👨‍💻 Developer: kaddu"
        )

        await update.message.reply_text(result)

    except:
        await update.message.reply_text("❌ API error. Try again later.")


# ---------- ADMIN COMMANDS ----------
async def maintenance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global MAINTENANCE
    if update.effective_user.id != ADMIN_ID:
        return

    if not context.args:
        await update.message.reply_text("Usage: /maintenance on | off")
        return

    MAINTENANCE = context.args[0].lower() == "on"
    await update.message.reply_text(
        "🛠 Maintenance ON" if MAINTENANCE else "✅ Maintenance OFF"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text(
        f"📊 BOT STATUS\n\nUsers: {len(USERS)}\nMaintenance: {MAINTENANCE}"
    )


# ---------- MAIN ----------
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("maintenance", maintenance))
    app.add_handler(CommandHandler("status", status))

    app.add_handler(CallbackQueryHandler(check_join, pattern="check_join"))
    app.add_handler(CallbackQueryHandler(info_button, pattern="info"))
    app.add_handler(CallbackQueryHandler(paid_glory, pattern="paid_glory"))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()

