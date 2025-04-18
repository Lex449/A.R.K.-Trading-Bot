from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    
    if isinstance(update, Update) and update.message:
        await update.message.reply_text("Ein unerwarteter Fehler ist aufgetreten.")