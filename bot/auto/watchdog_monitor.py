# bot/auto/watchdog_monitor.py

"""
A.R.K. Ultra Watchdog Monitor – Crash Detection Layer 2025
Autonomous Recovery System for Auto-Signal Loop.
"""

import asyncio
import logging
import time
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from bot.auto.watchdog_state import get_last_heartbeat  # <<< neu!

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

async def watchdog_monitor(application):
    """
    Monitors the heartbeat and restarts AutoSignalLoop on crash detection.
    """
    bot = application.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    logger.info("🛡️ [Watchdog] Monitor activated.")

    while True:
        try:
            last_heartbeat = get_last_heartbeat()
            time_since_last_heartbeat = time.time() - last_heartbeat

            if time_since_last_heartbeat > 90:
                logger.critical("⚠️ [Watchdog] Auto-Signal Loop heartbeat missing! Restart triggered.")
                await report_error(bot, chat_id, Exception("Auto-Signal Loop crashed. Restarting..."), context_info="Watchdog Crash Detection")

                from bot.auto.auto_signal_loop import auto_signal_loop  # << Importieren NUR im Fehlerfall (Lazy Import)
                asyncio.create_task(auto_signal_loop())

            await asyncio.sleep(30)

        except Exception as e:
            logger.critical(f"🔥 [Watchdog] Fatal Watchdog Monitor Error: {e}")
            await report_error(bot, chat_id, e, context_info="Fatal Watchdog Error")
            await asyncio.sleep(30)
