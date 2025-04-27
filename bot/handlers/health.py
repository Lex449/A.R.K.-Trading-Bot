from telegram import Update
from telegram.ext import ContextTypes

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        await update.message.reply_text("✅ Bot Status: Online and Healthy!")
    except Exception as e:
        await update.message.reply_text("❌ Bot Status: Critical Error!")
