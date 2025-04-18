# bot/handlers/status.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.utils.language import get_language

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    lang = get_language(update)

    messages = {
        "de": "📊 *Status:* A.R.K. ist bereit.\nWarte auf neue Marktbewegungen...",
        "en": "📊 *Status:* A.R.K. is active.\nWaiting for new market movements..."
    }

    await update.message.reply_text(messages[lang], parse_mode="Markdown")

status = CommandHandler("status", status)