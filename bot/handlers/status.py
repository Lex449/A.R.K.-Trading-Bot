from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.config.settings import get_settings

settings = get_settings()

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id != settings["DANIEL_TELEGRAM_ID"]:
        await update.message.reply_text("Access denied.")
        return

    status_text = (
        "*A.R.K. Statusbericht:*\n"
        "• Verbindung: ✅ stabil\n"
        "• Analysemodul: ✅ bereit\n"
        "• Signalmodul: ✅ einsatzfähig\n"
        "• Energielevel: ⚡️ 100 %\n\n"
        "_Alles läuft wie geschmiert._"
    )

    await update.message.reply_text(status_text, parse_mode="Markdown")

status_handler = CommandHandler("status", status_command)