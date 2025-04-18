from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from datetime import datetime

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.now().strftime("%H:%M:%S")
    await update.message.reply_text(f"Pong! Bot läuft.\nAktuelle Zeit: {now}")

ping_handler = CommandHandler("ping", ping)