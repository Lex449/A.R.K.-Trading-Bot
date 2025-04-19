from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from bot.config.settings import get_settings
from bot.utils.language import get_language

async def shutdown(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    settings = get_settings()
    lang = get_language(update)

    if str(update.effective_user.id) != str(settings["DANIEL_ID"]):
        messages = {
            "de": "⛔️ Nur autorisierte Benutzer dürfen den Bot stoppen.",
            "en": "⛔️ Only authorized users may shut down the bot."
        }
        await update.message.reply_text(messages[lang])
        return

    messages = {
        "de": "🛑 Bot wird jetzt beendet...",
        "en": "🛑 Shutting down the bot now..."
    }
    await update.message.reply_text(messages[lang])
    await context.application.stop()

shutdown_handler = CommandHandler("shutdown", shutdown)