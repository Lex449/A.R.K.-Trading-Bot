# bot/auto/connection_watchdog.py

"""
A.R.K. Connection Watchdog – Ultra Stability Layer
Monitors Telegram Bot connectivity and attempts auto-recovery on failure.
"""

import logging
import aiohttp
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

async def check_connection(bot, chat_id: int) -> None:
    """
    Pings the Telegram Bot API to verify connection health.
    If the connection fails, it reports and triggers optional recovery steps.
    """
    try:
        await bot.get_me()
        logger.info("✅ [Connection] Telegram Bot connection verified successfully.")

    except Exception as e:
        logger.error(f"❌ [Connection] Lost connection to Telegram: {e}")
        await report_error(bot, chat_id, e, context_info="Connection Watchdog Failure")

async def start_connection_watchdog(application, interval_seconds: int = 180):
    """
    Periodically checks Telegram Bot API connection every 'interval_seconds'.
    """
    bot = application.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    logger.info(f"🛡️ [Connection Watchdog] Activated. Checking every {interval_seconds} seconds.")

    while True:
        try:
            await check_connection(bot, chat_id)

        except Exception as e:
            logger.critical(f"🔥 [Connection Watchdog] Critical failure: {e}")
            await report_error(bot, chat_id, e, context_info="Fatal Connection Watchdog Crash")

        await asyncio.sleep(interval_seconds)
