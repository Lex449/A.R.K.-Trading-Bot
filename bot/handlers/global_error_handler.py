# bot/handlers/global_error_handler.py

"""
A.R.K. Global Error Handler – Ultra Premium Resilience Build 2025.
Captures and reports all unhandled errors reliably and bilingual.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Global catcher for ALL unhandled exceptions in the bot system.
    Reports critical errors safely via Telegram and local logs.
    """
    bot = context.bot
    fallback_chat_id = int(config["TELEGRAM_CHAT_ID"])
    chat_id = fallback_chat_id
    lang = "en"

    try:
        # Try to get the chat_id of the user if possible
        if update and hasattr(update, "effective_chat") and update.effective_chat:
            chat_id = update.effective_chat.id
            lang = get_language(chat_id) or "en"

        # The actual error
        error = context.error
        logger.error(f"⚠️ [GlobalError] {error}")

        # Report the error properly
        await report_error(bot, chat_id, error, context_info="Global Handler Exception")

        # Notify the user nicely if possible
        if update and hasattr(update, "message") and update.message:
            error_message = get_text("global_error_report", lang).format(error=str(error))
            await update.message.reply_text(error_message, parse_mode="Markdown")

        logger.info(f"✅ [GlobalErrorHandler] Error processed for Chat ID: {chat_id}")

    except Exception as fallback_error:
        # If the error handler itself fails (very rare)
        logger.critical(f"🔥 [Fatal Global Error Handler Crash] {repr(fallback_error)}")
        await report_error(bot, fallback_chat_id, fallback_error, context_info="Fatal Crash in Global Error Handler")
