from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hey! Ich bin dein A.R.K. Trading Mentor – bereit, loszulegen!")