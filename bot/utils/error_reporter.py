"""
A.R.K. Error Reporter – Premium Fehlerbehandlung.
Sichert alle Fehler ab: lokal & per Telegram.
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
    - Saves full traceback locally
    - Sends a summarized alert to Telegram

    Args:
        bot (Bot): Telegram Bot instance
        chat_id (int): Telegram chat id
        error (Exception): Caught error
        context_info (str): Optional context information
    """
    try:
        # === Build full error details ===
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
        full_error = (
            f"Timestamp: {timestamp}\n"
            f"Context: {context_info}\n"
            f"Error: {str(error)}\n"
            f"Traceback:\n{''.join(traceback.format_exception(type(error), error, error.__traceback__))}"
        )

        # Save full log to file
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(full_error + "\n" + "="*80 + "\n")

        logger.error(f"[Reported Error] {context_info} | {error}")

        # === Build Telegram alert ===
        short_error = (
            f"⚠️ *Critical Error*\n\n"
            f"*Context:* `{context_info}`\n"
            f"*Error:* `{str(error)}`\n"
            f"```{''.join(traceback.format_exception_only(type(error), error)).strip()}```"
        )

        if len(short_error) > 4000:
            short_error = short_error[:3990] + "`...`"

        await bot.send_message(chat_id=chat_id, text=short_error, parse_mode="Markdown")

    except Exception as e:
        logger.critical(f"[Error Reporting Failure] {e}")
