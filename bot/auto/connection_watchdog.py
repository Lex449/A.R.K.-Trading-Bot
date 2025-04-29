# bot/auto/connection_watchdog.py

"""
A.R.K. Connection Watchdog – Ultra Defense Layer.
Monitors Telegram Bot connection health and reports critical failures.
"""

import logging
from telegram import Bot
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

async def check_connection(bot: Bot, chat_id: int) -> None:
    """
    Verifies Telegram Bot API connectivity by calling get_me().
    Reports immediately if connection issues are detected.

    Args:
        bot (Bot): Telegram Bot instance.
        chat_id (int): Telegram chat ID for error reporting.
    """
    try:
        await bot.get_me()
        logger.info("✅ [Connection Watchdog] Telegram connection verified successfully.")

    except Exception as e:
        logger.error(f"❌ [Connection Watchdog] Telegram connection check failed: {e}")
        await report_error(bot, chat_id, e, context_info="Telegram Connection Failure")

        try:
            await bot.send_message(
                chat_id=chat_id,
                text="⚠️ *Critical Warning:* Telegram connection temporarily lost. Attempting to stabilize...",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            logger.info("✅ [Connection Watchdog] Alert message sent to user.")

        except Exception as alert_error:
            logger.critical(f"🔥 [Connection Watchdog FATAL] Failed to send alert message: {alert_error}")
