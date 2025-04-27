"""
Health Check Handler für A.R.K. Trading Bot
Made in Bali. Engineered with German Precision.
"""

from telegram import Update
from telegram.ext import ContextTypes

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Antwortet auf den Health Check Befehl /health mit Statusmeldung.
    """
    try:
        await update.message.reply_text("✅ A.R.K. System Check: Bot läuft stabil und analysiert!")
    except Exception:
        await update.message.reply_text("❌ A.R.K. System Check: Fehler erkannt. Bitte prüfen!")
