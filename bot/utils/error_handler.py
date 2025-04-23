import logging
import traceback

logger = logging.getLogger(__name__)

async def handle_error(update, context):
    error_trace = traceback.format_exc()
    logger.error("❌ Fehler aufgetreten:\n%s", error_trace)

    try:
        if update and getattr(update, "message", None):
            await update.message.reply_text("❌ Interner Fehler. A.R.K. wurde informiert.")
        elif update and getattr(update, "callback_query", None):
            await update.callback_query.answer("❌ Fehler!", show_alert=True)
    except Exception as notify_error:
        logger.error("Fehler bei der Fehlerbenachrichtigung: %s", notify_error)
