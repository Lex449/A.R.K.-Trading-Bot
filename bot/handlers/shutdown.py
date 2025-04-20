from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    message = (
        f"⛔️ A.R.K. wird jetzt heruntergefahren...\n"
        f"👤 Angefordert von: {user.first_name}"
    )
    await update.message.reply_text(message)
    await context.application.stop()

shutdown_handler = CommandHandler("shutdown", shutdown)