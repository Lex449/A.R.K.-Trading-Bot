from telegram import Update
from telegram.ext import ContextTypes

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Willkommen bei A.R.K. – deinem Trading-Mentor. Gib /signal oder /analyse ein, um zu starten.")