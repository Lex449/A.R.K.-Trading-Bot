from telegram import Update
from telegram.ext import ContextTypes

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ A.R.K. ist online und bereit.")