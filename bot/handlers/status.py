from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "📊 *A.R.K. Systemstatus*\n\n"
        "• Bot: Online & fokussiert\n"
        "• Analysemodul: Aktiv\n"
        "• Signalqualität: Bewertet mit ⭐️\n"
        "• Sprache: Automatische Erkennung (DE/EN)"
    )
    await update.message.reply_markdown(msg)

status_handler = CommandHandler("status", status)