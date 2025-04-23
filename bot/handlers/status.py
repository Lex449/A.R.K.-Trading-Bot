# bot/handlers/status.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Antwortet auf /status mit dem aktuellen Bot-Status."""
    await update.message.reply_text(
        "✅ *A.R.K. Status:*\n"
        "Der Bot läuft stabil, überwacht die Märkte live und ist bereit für Signale.\n"
        "_Engine: TwelveData + techn. Analyse_\n"
        "_Interface: Telegram | Sprache: DE+EN_",
        parse_mode="Markdown"
    )

status_handler = CommandHandler("status", status)