import logging
import traceback
import os
from telegram import Bot
from datetime import datetime

# === Setup Logging ===
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Logfile-Pfad
LOG_DIR = "logs"
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")

# Stelle sicher, dass der Log-Ordner existiert
os.makedirs(LOG_DIR, exist_ok=True)

async def report_error(bot: Bot, chat_id: int, error: Exception, context_info: str = ""):
    """
    Sends an error report to Telegram and logs it to a local file.
    """

    try:
        # Format Error Details
        error_summary = f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n"
        if context_info:
            error_summary += f"Context: {context_info}\n"
        error_summary += f"Error: {str(error)}\n"
        error_summary += "Traceback:\n" + "".join(traceback.format_exception(type(error), error, error.__traceback__))

        # Log into File
        with open(ERROR_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(error_summary + "\n" + "="*80 + "\n")

        # Prepare Short Message for Telegram
        telegram_message = (
            f"⚠️ *Error Report*\n\n"
            f"*Context:* `{context_info}`\n"
            f"*Error:* `{str(error)}`\n"
            f"```{''.join(traceback.format_exception_only(type(error), error))}```"
        )

        # Shorten if necessary (Telegram max message size)
        if len(telegram_message) > 4000:
            telegram_message = telegram_message[:3990] + "`...`"

        await bot.send_message(chat_id=chat_id, text=telegram_message, parse_mode="Markdown")

        logger.error(f"[Reported Error] Context: {context_info} | Error: {str(error)}")

    except Exception as e:
        logger.critical(f"[Error Reporting Failure] {e}")
