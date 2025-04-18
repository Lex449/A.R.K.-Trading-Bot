from telegram import Update
from telegram.ext import ContextTypes

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ich analysiere die Märkte live...\n"
        "Bitte kurz warten – ich melde mich mit dem besten Setup!"
    )