# bot/handlers/shutdown.py

from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
import logging

# Nur autorisierte User dürfen den Bot stoppen – Daniel only
ALLOWED_USER_IDS = [7699862580]

shutdown_handler = CommandHandler("shutdown", lambda update, context: shutdown(update, context))

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in ALLOWED_USER_IDS:
        await update.message.reply_text("❌ Zugriff verweigert. Nur für Administratoren.")
        logging.warning(f"[SHUTDOWN] Unberechtigter Zugriff: {user_id}")
        return

    try:
        await update.message.reply_text(
            "🛑 *A.R.K. wird heruntergefahren...*\n"
            "_System sicher beendet – morgen wieder bereit._",
            parse_mode="Markdown"
        )
        logging.info("[SHUTDOWN] Bot wurde regulär beendet.")
        await context.application.stop()
    except Exception as e:
        logging.error(f"[SHUTDOWN ERROR] {e}")
        await update.message.reply_text("❌ Fehler beim Shutdown. Bitte manuell prüfen.")
