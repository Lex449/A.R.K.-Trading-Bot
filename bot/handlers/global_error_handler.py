# bot/handlers/error_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Catches and reports ALL unhandled errors globally with ultra-resilience.
    """

    chat_id = int(config["TELEGRAM_CHAT_ID"])
    lang = "en"

    try:
        # Safe fallback: Check if update and effective_chat exist
        if update and hasattr(update, "effective_chat") and update.effective_chat:
            chat_id = update.effective_chat.id
            lang = get_language(chat_id) or "en"

        error = context.error

        logger.error(f"⚠️ [Global Error] {error}")

        # Send full technical error report to admin
        await report_error(context.bot, chat_id, error, context_info="Global Bot Error")

        # Optional: Notify user if update.message exists
        if update and hasattr(update, "message") and update.message:
            error_message = get_text("global_error_report", lang).format(error=str(error))
            await update.message.reply_text(error_message, parse_mode="Markdown")

        logger.info(f"⚠️ [Error Handler] Error successfully processed for chat ID: {chat_id}")

    except Exception as critical_failure:
        logger.critical(f"🚨 [Critical Failure] Error inside Global Error Handler: {critical_failure}")
        await report_error(context.bot, chat_id, critical_failure, context_info="Critical Failure in Global Error Handler")
