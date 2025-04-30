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
    Reports an exception via Telegram and logs it.

    Args:
        bot (Bot): The Telegram bot instance.
        chat_id (int): Admin chat ID for error reporting.
        error (Exception): Exception object.
        context_info (str): Context where error occurred.
    """
    try:
        # Clean traceback and escape backticks
        tb_clean = traceback.format_exc().replace('`', "'")
        error_safe = str(error).replace('`', "'")
        context_safe = context_info.replace('`', "'")

        error_text = (
            f"⚠️ *A.R.K. Error Report*\n\n"
            f"*Context:* `{context_safe}`\n"
            f"*Error:* `{error_safe}`\n\n"
            f"*Traceback:*\n```{tb_clean}```"
        )

        await bot.send_message(chat_id=chat_id, text=error_text, parse_mode="Markdown")
        logger.error(f"[ErrorReporter] Exception reported: {error_safe} | Context: {context_safe}")

    except Exception as reporting_error:
        logger.critical(f"[ErrorReporter] Failed to send error report: {repr(reporting_error)}")
