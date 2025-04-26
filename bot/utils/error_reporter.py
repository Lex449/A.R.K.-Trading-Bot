# bot/utils/error_reporter.py

import logging
import traceback
from telegram import Bot

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def report_error(bot: Bot, chat_id: int, error: Exception, context_info: str = ""):
    """
    Sends an error report to a specified Telegram chat.

    Args:
        bot (Bot): The Telegram Bot instance.
        chat_id (int): Telegram Chat ID for error reports.
        error (Exception): The exception that occurred.
        context_info (str): Additional context about where the error happened.
    """
    try:
        error_message = f"⚠️ *Error Report*\n\n"
        if context_info:
            error_message += f"Context: `{context_info}`\n"
        error_message += f"Error: `{str(error)}`\n"
        error_message += f"Traceback:\n`{traceback.format_exc()}`"

        await bot.send_message(chat_id=chat_id, text=error_message, parse_mode="Markdown")
        logger.error(f"Reported error: {error}")

    except Exception as e:
        logger.critical(f"Failed to send error report: {e}")
