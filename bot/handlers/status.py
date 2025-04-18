from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "✅ *A.R.K. Status*\n"
        "• Online: Ja\n"
        "• Signalmodul: Aktiv\n"
        "• Analyse: Aktiv\n"
        "• Spracherkennung: Auto (DE/EN)"
    )
    await update.message.reply_markdown(text)

status_handler = CommandHandler("status", status)