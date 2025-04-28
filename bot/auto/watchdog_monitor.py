"""
A.R.K. Ultra Watchdog Monitor – 2025 Version
Autonomous Crash Detection and Recovery System
"""

import asyncio
import logging
import time
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup Structured Logger
logger = setup_logger(__name__)
config = get_settings()

# === Internal Monitoring State ===
_last_heartbeat = time.time()

def refresh_watchdog():
    """
    Should be called periodically inside auto_signal_loop to update the heartbeat.
    """
    global _last_heartbeat
    _last_heartbeat = time.time()

async def watchdog_monitor(application):
    """
    Monitors the auto_signal_loop and restarts it if crash is detected.
    """
    bot = application.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    logger.info("🛡️ [Watchdog] Watchdog Monitor activated.")

    while True:
        try:
            time_since_last_heartbeat = time.time() - _last_heartbeat

            if time_since_last_heartbeat > 90:
                logger.error(f"⚠️ [Watchdog] Detected signal loop crash! Restarting...")
                await report_error(bot, chat_id, Exception("Auto-Signal Loop crashed. Auto-restarting..."), context_info="Watchdog Crash Detection")

                # Restart the Auto Signal Loop
                asyncio.create_task(auto_signal_loop())
                refresh_watchdog()

            await asyncio.sleep(30)  # Check every 30 seconds

        except Exception as e:
            logger.critical(f"🔥 [Watchdog] Fatal Error: {e}")
            await report_error(bot, chat_id, e, context_info="Fatal Watchdog Error")
            await asyncio.sleep(30)
