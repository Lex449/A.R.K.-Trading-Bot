"""
A.R.K. Global Error Handler – Ultra Stable Core.
Gracefully catches and reports all unexpected Telegram exceptions.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup Logger
logger = logging.getLogger(__name__)
config = get_settings()

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Catches and reports ALL unhandled errors from the Telegram application.
    Guarantees maximum bot uptime and smooth crash reporting.
    """
    try:
        error = context.error
        chat_id = int(config["TELEGRAM_CHAT_ID"])

        logger.error(f"⚠️ [Global Error] {error}")

        # Report the error via Telegram
        await report_error(context.bot, chat_id, error, context_info="Global Bot Error")

    except Exception as critical_failure:
        logger.critical(f"🚨 [Critical Failure] Error inside Global Error Handler: {critical_failure}")
