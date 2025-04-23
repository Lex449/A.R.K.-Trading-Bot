from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def ping(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("✅ Bot is online! Ready for action.")

ping_handler = CommandHandler("ping", ping)