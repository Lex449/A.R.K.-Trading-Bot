import sys
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.config.settings import get_settings

settings = get_settings()

async def shutdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)

    if user_id != settings["DANIEL_TELEGRAM_ID"]:
        await update.message.reply_text("Access denied.")
        return

    await update.message.reply_text("🛑 A.R.K. wird heruntergefahren...")
    await context.bot.shutdown()
    sys.exit(0)

shutdown_handler = CommandHandler("shutdown", shutdown_command)