from telegram import Update
from telegram.ext import ContextTypes

async def handle_error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[FEHLER] {context.error}")
    if update and update.message:
        await update.message.reply_text("Ein unerwarteter Fehler ist aufgetreten.")