# bot/utils/error_reporter.py

"""
A.R.K. Error Reporter – Maximum Protection Build.
Saves all errors locally + Telegram instant alert.
"""

import os
import logging
import traceback
from datetime import datetime
from telegram import Bot
from bot.utils.logger import setup_logger

# === Setup Logger ===
logger = setup_logger(__name__)

# === Error Log Directory ===
LOG_DIR = "logs"
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
os.makedirs(LOG_DIR, exist_ok=True)

async def report_error(bot: Bot, chat_id: int, error: Exception, context_info: str = ""):
    """
    Reports critical errors:
    - Saves full traceback locally (.log)
    - Sends a summarized alert via Telegram
    """
    try:
        # === Build full error details for local saving ===
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        full_error = (
            f"Timestamp: {timestamp}\n"
            f"Context: {context_info}\n"
            f"Error: {str(error)}\n"
            f"Traceback:\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}"
        )

        # === Save detailed error to local file ===
        with open(ERROR_LOG_FILE, "a", encoding="utf-8", errors="ignore") as f:
            f.write(full_error + "\n" + "="*80 + "\n")

        logger.error(f"[Reported Error] {context_info} | {error}")

        # === Build Telegram short alert ===
        short_error = (
            f"⚠️ *Critical Bot Error*\n\n"
            f"*Context:* `{context_info}`\n"
            f"*Error:* `{str(error)}`\n"
            f"```\n{''.join(traceback.format_exception_only(type(error), error))}\n```"
        )

        # Telegram size limit handling
        if len(short_error) > 3990:
            short_error = short_error[:3990] + "\n```...```"

        await bot.send_message(chat_id=chat_id, text=short_error, parse_mode="Markdown")

    except Exception as fallback_error:
        logger.critical(f"[Error Reporting FATAL] {fallback_error}")
