"""
A.R.K. Global Error Handler
Fängt ALLE nicht abgefangenen Telegram-Fehler elegant ab.
"""

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup Logger
logger = logging.getLogger(__name__)
config = get_settings()

async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all unexpected errors gracefully.
    """
    try:
        # Capture full exception
        error = context.error
        chat_id = int(config["TELEGRAM_CHAT_ID"])

        logger.error(f"[Global Error] {error}")

        # Report via Error Reporter
        await report_error(context.bot, chat_id, error, context_info="Global Bot Error")

    except Exception as e:
        logger.critical(f"[Critical Global Error] {e}")
