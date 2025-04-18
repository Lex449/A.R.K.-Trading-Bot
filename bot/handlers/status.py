from telegram import Update
from telegram.ext import ContextTypes

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Status: A.R.K. ist aktiv und überwacht die Märkte.")