# bot/utils/error_reporter.py

"""
Handles critical error reporting:
1. Logs detailed traceback into a local file.
2. Sends a summarized error report via Telegram.
"""

import os
import logging
import traceback
from datetime import datetime
from telegram import Bot
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Logfile configuration
LOG_DIR = "logs"
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

async def report_error(bot: Bot, chat_id: int, error: Exception, context_info: str = ""):
    """
    Reports an error:
    - Saves full details locally in error.log
    - Sends a condensed report to Telegram

    Args:
        bot (Bot): Telegram Bot instance.
        chat_id (int): Target Telegram chat ID.
        error (Exception): The caught exception.
        context_info (str): Optional contextual information.
    """
    try:
        # === Prepare full error log entry ===
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        error_details = (
            f"Timestamp: {timestamp}\n"
            f"Context: {context_info}\n"
            f"Error: {str(error)}\n"
            f"Traceback:\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}"
        )

        # Save full log to file
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(error_details + "\n" + "="*100 + "\n")

        logger.error(f"[Reported Error] Context: {context_info} | Error: {error}")

        # === Prepare Telegram Message ===
        telegram_message = (
            f"⚠️ *Error Report*\n\n"
            f"*Context:* `{context_info}`\n"
            f"*Error:* `{str(error)}`\n"
            f"```{''.join(traceback.format_exception_only(type(error), error)).strip()}```"
        )

        if len(telegram_message) > 4000:
            telegram_message = telegram_message[:3990] + "`...`"

        await bot.send_message(chat_id=chat_id, text=telegram_message, parse_mode="Markdown")

    except Exception as e:
        logger.critical(f"[Error Reporting Failure] {e}")
