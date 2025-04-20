from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📊 Tageszusammenfassung wird vorbereitet...\nDieses Feature ist bald verfügbar!"
    )

recap_handler = CommandHandler("recap", recap)