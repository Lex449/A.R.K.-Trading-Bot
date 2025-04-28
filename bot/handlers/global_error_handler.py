"""
A.R.K. Global Error Handler – Ultra Diamond Resilience 2025.
Captures and reports all unhandled errors safely.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

# Setup Structured Logger
logger = setup_logger(__name__)
config = get_settings()

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Global catcher for ALL unhandled exceptions in the bot system.
    Ensures full protection and instant reporting.
    """
    bot = context.bot
    fallback_chat_id = int(config["TELEGRAM_CHAT_ID"])
    chat_id = fallback_chat_id
    lang = "en"

    try:
        # Safely extract user chat ID
        if update and hasattr(update, "effective_chat") and update.effective_chat:
            chat_id = update.effective_chat.id
            lang = get_language(chat_id) or "en"

        error = context.error
        logger.error(f"⚠️ [GlobalError] {error}")

        # Report error to Telegram + Local Log
        await report_error(bot, chat_id, error, context_info="Global Handler Exception")

        # Notify user if possible
        if update and hasattr(update, "message") and update.message:
            error_message = get_text("global_error_report", lang).format(error=str(error))
            await update.message.reply_text(error_message, parse_mode="Markdown")

        logger.info(f"✅ [ErrorHandler] Error successfully processed for Chat ID: {chat_id}")

    except Exception as fallback_error:
        # Fatal fallback if the error handler itself crashes
        logger.critical(f"🔥 [Fatal Error in GlobalErrorHandler] {repr(fallback_error)}")
        await report_error(bot, fallback_chat_id, fallback_error, context_info="Fatal Crash in Error Handler")
