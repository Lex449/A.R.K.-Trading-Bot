from telegram import Update
from telegram.ext import ContextTypes
from bot.config.settings import get_settings

settings = get_settings()

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if user_id != settings["DANIEL_TELEGRAM_ID"]:
        await update.message.reply_text("⛔ Du bist nicht autorisiert, mich zu stoppen.")
        return

    await update.message.reply_text("🛑 Ich beende den Dienst. Du weißt, wo du mich findest.")
    await context.application.stop()