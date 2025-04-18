from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.config.settings import get_settings

settings = get_settings()

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id != settings["DANIEL_TELEGRAM_ID"]:
        await update.message.reply_text("Access denied.")
        return

    await update.message.reply_text("✅ Pong! Die Verbindung steht.")

ping_handler = CommandHandler("ping", ping_command)