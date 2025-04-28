"""
A.R.K. Connection Watchdog – Ultra Stability Layer
Monitors Telegram Bot connectivity and attempts auto-recovery on failure.
"""

import logging
from telegram import Bot
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup Logger
logger = setup_logger(__name__)

# Load Settings
config = get_settings()

async def check_connection(bot: Bot, chat_id: int):
    """
    Pings the Telegram Bot API to verify connection health.
    If failed, reports and optionally triggers recovery.
    """
    try:
        await bot.get_me()
        logger.info("✅ [Watchdog] Telegram Bot connection verified successfully.")

    except Exception as e:
        logger.error(f"❌ [Watchdog] Connection lost: {e}")
        await report_error(bot, chat_id, e, context_info="Connection Watchdog Failure")

        # Optional: Emergency Recovery Actions (nur vorbereiten)
        # await restart_application()
