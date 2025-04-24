# /bot/handlers/ping.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_language(update)

    if lang == "de":
        msg = "✅ *A.R.K. ist online und bereit!*"
    else:
        msg = "✅ *A.R.K. is online and ready!*"

    await update.message.reply_markdown(msg)

# === Handler exportieren ===
ping_handler = CommandHandler("ping", ping)
