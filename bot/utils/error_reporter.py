# bot/utils/error_reporter.py

"""
A.R.K. Error Reporter – Intelligent Exception Management 2025.
Automatically reports critical errors to the admin via Telegram and logs them locally.
"""

import traceback
from telegram import Bot
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup logger
logger = setup_logger(__name__)
config = get_settings()

async def report_error(bot: Bot, chat_id: int, error: Exception, context_info: str = "Unknown Context") -> None:
    """
    Reports an exception via Telegram and logs it locally.
    Args:
        bot (Bot): The Telegram bot instance.
        chat_id (int): The chat ID to send the report to.
        error (Exception): The actual exception.
        context_info (str): Additional context where the error happened.
    """
    try:
        error_text = (
            f"⚠️ *A.R.K. Error Report*\n\n"
            f"*Context:* {context_info}\n"
            f"*Error:* `{str(error)}`\n\n"
            f"*Traceback:*\n```{traceback.format_exc()}```"
        )

        # Send detailed error to admin
        await bot.send_message(chat_id=chat_id, text=error_text, parse_mode="Markdown")
        logger.error(f"Error reported to Admin (Chat ID {chat_id}): {error_text}")

    except Exception as reporting_error:
        # If even reporting fails
        logger.critical(f"Critical Error while reporting error: {repr(reporting_error)}")
