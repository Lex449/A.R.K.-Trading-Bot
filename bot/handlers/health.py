from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text

async def health_check(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Responds to the /health command.
    Bilingual, stable, minimalistic.
    """
    chat_id = update.effective_chat.id
    lang = get_language(chat_id) or "en"  # Get the preferred language of the user, defaulting to 'en'

    try:
        # Send health check success message
        health_message = get_text("health_ok", lang)  # Health check success message
        await update.message.reply_text(health_message, parse_mode="Markdown")

    except Exception as e:
        # Send failure message in case of an error
        error_message = get_text("health_fail", lang)  # Health check failure message
        await update.message.reply_text(error_message, parse_mode="Markdown")

        # Log the error for further investigation (raise to trigger global error handler)
        raise Exception(f"Health check failed: {str(e)}")
