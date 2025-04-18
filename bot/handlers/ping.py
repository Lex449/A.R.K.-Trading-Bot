from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Ich bin da – motiviert, bereit und voll fokussiert. Sag, was du brauchst!")

ping_handler = CommandHandler("ping", ping)