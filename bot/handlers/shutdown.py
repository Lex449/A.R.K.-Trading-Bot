# bot/handlers/shutdown.py
# Handler zum sicheren Herunterfahren des Bots durch Admin

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import logging

# Optional: Admin-ID einschränken
ALLOWED_USER_IDS = [7699862580]  # Daniel Hein

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("❌ Zugriff verweigert: Du bist nicht autorisiert, den Bot zu stoppen.")
        logging.warning(f"Shutdown-Versuch durch nicht autorisierten User: {user_id}")
        return

    try:
        await update.message.reply_text("⚠️ Der Bot wird jetzt sicher heruntergefahren...\nDanke für deine Arbeit heute, Commander.")
        logging.info("Bot-Shutdown durch Admin ausgelöst.")
        await context.application.stop()
    except Exception as e:
        logging.error(f"❌ Fehler beim Shutdown: {e}")
        await update.message.reply_text("❌ Beim Shutdown ist ein Fehler aufgetreten.")

shutdown_handler = CommandHandler("shutdown", shutdown)