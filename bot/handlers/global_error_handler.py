"""
A.R.K. Global Error Handler – Ultra Premium Resilience Build 2025
Captures and reports all unhandled exceptions in a multilingual, structured and fault-tolerant way.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger and config
logger = setup_logger(__name__)
config = get_settings()

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Catches ALL unhandled errors in the system.
    Ensures graceful reporting and user notification.
    """
    bot = context.bot
    fallback_chat_id = int(config["TELEGRAM_CHAT_ID"])
    chat_id = fallback_chat_id
    lang = "en"

    try:
        # Attempt to extract user context
        if update and hasattr(update, "effective_chat") and update.effective_chat:
            chat_id = update.effective_chat.id
            lang = get_language(chat_id) or "en"

        # Capture the actual error
        error = context.error
        logger.error(f"⚠️ [GlobalError] {repr(error)}")

        # Report to admin
        await report_error(bot, chat_id, error, context_info="Global Handler Exception")

        # Notify user (if possible)
        if update and hasattr(update, "message") and update.message:
            error_message = get_text("global_error_report", lang).format(error=str(error))
            await update.message.reply_text(error_message, parse_mode="Markdown")

        logger.info(f"✅ [GlobalErrorHandler] Handled & reported for Chat ID: {chat_id}")

    except Exception as fatal:
        # If error handler itself fails
        logger.critical(f"🔥 [Fatal Global Error Handler Crash] {repr(fatal)}")
        await report_error(bot, fallback_chat_id, fatal, context_info="Fatal Crash in Global Error Handler")
