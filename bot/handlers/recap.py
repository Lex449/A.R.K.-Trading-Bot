from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def recap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "🔁 *A.R.K. Daily Recap*
"
        "Hier ist deine tägliche Zusammenfassung. "
        "Feature ist in Entwicklung und bald verfügbar – stay tuned!"
    )
    await update.message.reply_text(message, parse_mode="Markdown")

recap_handler = CommandHandler("recap", recap)