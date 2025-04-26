# bot/utils/error_reporter.py

import logging
import traceback
from telegram import Bot

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def report_error(bot: Bot, chat_id: int, exception: Exception, context_info: str = ""):
    """
    Reports an error by sending a detailed, human-readable message to Telegram
    and logging it server-side.

    Args:
        bot (Bot): Telegram Bot instance.
        chat_id (int): Target Telegram Chat ID.
        exception (Exception): The raised exception.
        context_info (str): Optional context description.
    """
    try:
        # Create detailed traceback
        error_trace = ''.join(traceback.format_exception(None, exception, exception.__traceback__))

        # Prepare Telegram message
        error_message = (
            f"⚠️ *Error Report*\n\n"
            f"*Context:* `{context_info}`\n"
            f"*Error:* `{str(exception)}`\n\n"
            f"*Traceback:*\n```{error_trace[-3000:]}```"
        )

        # Send message to Telegram
        await bot.send_message(chat_id=chat_id, text=error_message, parse_mode="Markdown")

        # Log full error server-side
        logger.error(f"[ERROR CONTEXT] {context_info}")
        logger.error(f"[ERROR] {str(exception)}")
        logger.error(f"[TRACEBACK]\n{error_trace}")

    except Exception as reporting_error:
        logger.critical(f"Error while trying to report an error: {reporting_error}")
