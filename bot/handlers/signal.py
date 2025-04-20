from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📡 Signal wird abgerufen...\nBitte einen Moment Geduld. Du erhältst gleich dein Markt-Update!"
    )

signal_handler = CommandHandler("signal", signal)