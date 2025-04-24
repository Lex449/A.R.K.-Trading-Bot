# /bot/handlers/shutdown.py

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import logging

ALLOWED_USER_IDS = [7699862580]  # Daniel Hein

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Beendet den Bot sicher – nur für autorisierte User."""
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("❌ Zugriff verweigert: Du bist nicht autorisiert, den Bot zu stoppen.")
        logging.warning(f"⚠️ Unerlaubter Shutdown-Versuch durch User-ID: {user_id}")
        return

    try:
        await update.message.reply_text("🛑 Bot wird jetzt sicher heruntergefahren.\nDanke für deinen Einsatz, Commander.")
        logging.info("✅ Shutdown durch Admin erfolgreich.")
        await context.application.stop()
    except Exception as e:
        logging.error(f"❌ Shutdown-Fehler: {e}")
        await update.message.reply_text("❌ Fehler beim Shutdown – bitte manuell prüfen.")

# === Handler exportieren ===
shutdown_handler = CommandHandler("shutdown", shutdown)
