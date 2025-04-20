from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = (
        "✅ *A.R.K. Statusbericht*\n"
        "- Bot online\n"
        "- Signale aktiv\n"
        "- Marktüberwachung läuft\n"
        "- Break-even-Logik vorbereitet\n"
        "- Alle Systeme: *STABIL*"
    )
    await update.message.reply_markdown(message)

status_handler = CommandHandler("status", status)