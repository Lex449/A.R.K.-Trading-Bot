from telegram import Update
from telegram.ext import ContextTypes

async def handle_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if isinstance(update, Update) and update.message:
            await update.message.reply_text("Ein unerwarteter Fehler ist aufgetreten.")
    except Exception as e:
        print(f"Fehler beim Senden der Fehlermeldung: {e}")