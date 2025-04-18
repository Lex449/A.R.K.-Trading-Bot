from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.config.settings import get_settings
import sys

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_id = get_settings()["telegram"]["admin_id"]
    if update.effective_user.id != admin_id:
        await update.message.reply_text("❌ Du bist nicht autorisiert, mich zu beenden.")
        return

    await update.message.reply_text("🛑 A.R.K. wird beendet – bis bald, Mentor offline...")
    sys.exit()

shutdown_handler = CommandHandler("shutdown", shutdown)