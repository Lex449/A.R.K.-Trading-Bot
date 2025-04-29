"""
A.R.K. Global Error Handler – Ultra Diamond Resilience Build 2025.
Captures and reports all unhandled errors safely.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup Structured Logger
logger = setup_logger(__name__)
config = get_settings()

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Global catcher for all unhandled exceptions in the bot system.
    Ensures full resilience and instant reporting.
    """
    bot = context.bot
    fallback_chat_id = int(config["TELEGRAM_CHAT_ID"])
    chat_id = fallback_chat_id
    lang = "en"

    try:
        # Try to extract user chat ID
        if update and hasattr(update, "effective_chat") and update.effective_chat:
            chat_id = update.effective_chat.id
            lang = get_language(chat_id) or "en"

        error = context.error
        logger.error(f"⚠️ [GlobalError] {repr(error)}")

        # Send error report
        await report_error(bot, chat_id, error, context_info="Global Handler Exception")

        # Notify user if possible
        if update and hasattr(update, "message") and update.message:
            error_message = get_text("global_error_report", lang).format(error=str(error))
            await update.message.reply_text(
                error_message,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )

        logger.info(f"✅ [ErrorHandler] Error successfully processed for Chat ID: {chat_id}")

    except Exception as fatal_error:
        # Fatal fallback if error handling itself crashes
        logger.critical(f"🔥 [Fatal Error in Global Error Handler] {repr(fatal_error)}")
        try:
            await report_error(bot, fallback_chat_id, fatal_error, context_info="Fatal Crash in Error Handler")
        except Exception:
            pass  # Absolute fallback: ignore if report fails
