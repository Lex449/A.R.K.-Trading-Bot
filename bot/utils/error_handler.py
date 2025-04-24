import logging
import traceback
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger("A.R.K. ErrorHandler")

async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    error_trace = traceback.format_exc()
    logger.error("❌ Fehler aufgetreten:\n%s", error_trace)

    # Kontextdetails loggen
    if update:
        user_info = None
        if getattr(update, "message", None):
            user = update.message.from_user
            user_info = f"{user.username} | {user.id}"
        elif getattr(update, "callback_query", None):
            user = update.callback_query.from_user
            user_info = f"{user.username} | {user.id}"
        
        logger.warning("Fehlermeldung von: %s", user_info or "Unbekannt")

    try:
        # Nutzer informieren – je nach Art des Fehlers
        if getattr(update, "message", None):
            await update.message.reply_text("❌ Interner Fehler. A.R.K. wurde informiert.")
        elif getattr(update, "callback_query", None):
            await update.callback_query.answer("❌ Fehler erkannt – A.R.K. kümmert sich.", show_alert=True)

    except Exception as notify_error:
        logger.error("Fehler bei der Benutzerbenachrichtigung: %s", notify_error)
