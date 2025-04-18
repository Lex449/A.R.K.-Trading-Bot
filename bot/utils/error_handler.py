# bot/utils/error_handler.py

from telegram import Update
from telegram.ext import CallbackContext

async def handle_error(update: Update, context: CallbackContext) -> None:
    """Fehlerbehandlung für den Bot."""
    try:
        raise context.error
    except Exception as e:
        print(f"[ERROR]: {e}")
        if update:
            await update.message.reply_text("Es gab einen Fehler beim Ausführen des Befehls.")