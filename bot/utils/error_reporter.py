"""
A.R.K. Error Reporter – Ultra Maximum Protection Suite 2.0
Dual System: Local Log + Real-Time Telegram Alert.
Built for unstoppable error transparency and protection.
"""

import os
import logging
import traceback
from datetime import datetime
from telegram import Bot
from bot.utils.logger import setup_logger

# === Setup Structured Logger ===
logger = setup_logger(__name__)

# === Local Error Log Path ===
LOG_DIR = "logs"
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
os.makedirs(LOG_DIR, exist_ok=True)

async def report_error(bot: Bot, chat_id: int, error: Exception, context_info: str = "") -> None:
    """
    Handles error reporting:
    - Saves detailed traceback locally (.log)
    - Sends compact, clean Telegram alert
    """

    try:
        # === Build Full Local Error Log ===
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        error_details = (
            f"Timestamp: {timestamp}\n"
            f"Context: {context_info}\n"
            f"Error: {repr(error)}\n"
            f"Traceback:\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}"
        )

        # Save error locally
        with open(ERROR_LOG_FILE, "a", encoding="utf-8", errors="ignore") as file:
            file.write(error_details + "\n" + "="*100 + "\n")

        logger.error(f"[Reported Error] Context: {context_info} | {repr(error)}")

        # === Build Short Telegram Alert ===
        short_error = (
            f"⚠️ *Critical Bot Error*\n\n"
            f"*Context:* `{context_info}`\n"
            f"*Error:* `{str(error)}`\n"
            f"```{''.join(traceback.format_exception_only(type(error), error)).strip()}```"
        )

        # Handle Telegram size limits
        if len(short_error) > 3900:
            short_error = short_error[:3900] + "\n```...truncated```"

        await bot.send_message(chat_id=chat_id, text=short_error, parse_mode="Markdown")

    except Exception as fallback_error:
        # Ultimate fallback (last defense layer)
        logger.critical(f"🔥 [Fatal Error in ErrorReporter] {repr(fallback_error)}")
