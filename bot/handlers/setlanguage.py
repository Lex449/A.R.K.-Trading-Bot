# bot/handlers/setlanguage.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /setlanguage command.
    Lets users change their preferred language dynamically.
    """
    user = update.effective_user.first_name or "Trader"
    chat_id = update.effective_chat.id

    try:
        if not context.args:
            await update.message.reply_text("Please provide a language code (e.g., 'de' or 'en').")
            logger.warning(f"/setlanguage called without argument by {user}.")
            return

        choice = context.args[0].lower()

        if choice in ("de", "deutsch"):
            lang = "de"
        elif choice in ("en", "english"):
            lang = "en"
        else:
            await update.message.reply_text("Unknown language. Supported options: 'de', 'en'.")
            logger.warning(f"/setlanguage called with invalid input: {choice} by {user}")
            return

        context.user_data["lang"] = lang
        confirmation = get_text("set_language", lang)

        await update.message.reply_text(confirmation, parse_mode="Markdown")
        logger.info(f"Language changed to {lang} by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="/setlanguage command")
        logger.error(f"Error during /setlanguage command: {e}")
