# bot/utils/error_handler.py
import logging
import traceback

logger = logging.getLogger(__name__)

async def handle_error(update, context):
    """Fehlerbehandlung für alle Handler – Railway-kompatibel und stabil."""
    error_trace = traceback.format_exc()
    logger.error("❌ Fehler aufgetreten:\n%s", error_trace)

    try:
        if update and getattr(update, "message", None):
            await update.message.reply_text("❌ Ein interner Fehler ist aufgetreten. Wir kümmern uns darum.")
        elif update and getattr(update, "callback_query", None):
            await update.callback_query.answer("❌ Fehler aufgetreten.", show_alert=True)
    except Exception as notify_error:
        logger.error("Fehler bei der Fehlerbenachrichtigung: %s", notify_error)
