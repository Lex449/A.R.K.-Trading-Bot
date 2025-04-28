"""
A.R.K. Error Reporter – Absolute Defense Edition 2025.
Local Save + Instant Telegram Alert + Stability Shield.
"""

import os
import logging
import traceback
from datetime import datetime
from telegram import Bot
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Local Log Paths ===
LOG_DIR = "logs"
ERROR_LOG_FILE = os.path.join(LOG_DIR, "error.log")
os.makedirs(LOG_DIR, exist_ok=True)

async def report_error(bot: Bot, chat_id: int, error: Exception, context_info: str = "") -> None:
    """
    Full error reporting system:
    - Local trace log
    - Telegram instant alert
    - Hard-fallback in case Telegram fails
    """
    try:
        # === Timestamp ===
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        # === Full Traceback Build ===
        full_trace = ''.join(traceback.format_exception(type(error), error, error.__traceback__)).strip()

        # === Save to Local File ===
        detailed_log = (
            f"Timestamp: {timestamp}\n"
            f"Context: {context_info}\n"
            f"Error: {repr(error)}\n"
            f"Traceback:\n{full_trace}\n"
            + "=" * 120 + "\n"
        )

        with open(ERROR_LOG_FILE, "a", encoding="utf-8", errors="ignore") as f:
            f.write(detailed_log)

        logger.error(f"[Reported Error] Context: {context_info} | {repr(error)}")

        # === Build Telegram Alert (Safe Size) ===
        short_message = (
            f"⚠️ *Critical Error Detected*\n\n"
            f"*Context:* `{context_info}`\n"
            f"*Error:* `{str(error)}`\n"
            f"```{full_trace[:1500]}...```" if len(full_trace) > 1500 else f"```{full_trace}```"
        )

        if len(short_message) > 3900:
            short_message = short_message[:3900] + "\n```...truncated```"

        await bot.send_message(
            chat_id=chat_id,
            text=short_message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

    except Exception as fallback_error:
        # === Ultimate Self-Fallback ===
        fallback_message = (
            f"🔥 [ErrorReporter FATAL] Backup triggered:\n"
            f"Original Error Context: {context_info}\n"
            f"Original Error: {repr(error)}\n"
            f"Fallback Error: {repr(fallback_error)}"
        )

        logger.critical(fallback_message)

        try:
            await bot.send_message(
                chat_id=chat_id,
                text=f"🔥 *Fatal Error in ErrorReporter!*\n\n```{fallback_message}```",
                parse_mode="Markdown"
            )
        except Exception:
            # Not even Telegram works? Then it's logged only locally.
            pass
