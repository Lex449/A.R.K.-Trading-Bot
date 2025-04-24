# bot/handlers/shutdown.py

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.config.settings import get_settings
import logging

settings = get_settings()
ALLOWED_USER_IDS = [int(settings["TELEGRAM_CHAT_ID"])]

shutdown_handler = CommandHandler("shutdown", lambda update, context: shutdown(update, context))

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("❌ Zugriff verweigert. Nur für Administratoren.")
        logging.warning(f"[A.R.K. - SHUTDOWN] Unberechtigter Shutdown-Versuch von User-ID: {user_id}")
        return

    try:
        await update.message.reply_text(
            "🛑 *A.R.K. wird heruntergefahren...*\n"
            "_System sicher beendet – morgen wieder bereit._",
            parse_mode="Markdown"
        )
        logging.info("[A.R.K. - SHUTDOWN] Shutdown wurde erfolgreich durch autorisierten Benutzer ausgeführt.")
        await context.application.stop()
    except Exception as e:
        logging.error(f"[A.R.K. - SHUTDOWN ERROR] Shutdown fehlgeschlagen: {e}")
        await update.message.reply_text("❌ Fehler beim Shutdown. Bitte manuell prüfen.")
