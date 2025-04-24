# bot/handlers/ping.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_language(update)

    message = {
        "de": "✅ *A.R.K. ist online und bereit!*\n\nAlle Systeme laufen stabil. Du kannst jederzeit Signale empfangen.",
        "en": "✅ *A.R.K. is online and ready!*\n\nAll systems are running smoothly. You’re ready to receive signals."
    }

    await update.message.reply_markdown(message.get(lang, message["en"]))

# === Export ===
ping_handler = CommandHandler("ping", ping)
