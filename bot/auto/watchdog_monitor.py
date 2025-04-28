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
from bot.auto.watchdog_heartbeat import get_last_heartbeat  # Importiere die Funktion für den Heartbeat

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

            # Wenn der Heartbeat zu lange fehlt, starten wir den Auto-Signal-Loop neu
            if time_since_last_heartbeat > 90:
                logger.critical("⚠️ [Watchdog] Auto-Signal Loop heartbeat missing! Restart triggered.")
                await report_error(bot, chat_id, Exception("Auto-Signal Loop crashed. Restarting..."), context_info="Watchdog Crash Detection")

                # Lazy Import von `auto_signal_loop` im Fehlerfall und Neustart
                from bot.auto.auto_signal_loop import auto_signal_loop
                asyncio.create_task(auto_signal_loop())

            await asyncio.sleep(30)  # Warten 30 Sekunden und überprüfe dann erneut

        except Exception as e:
            logger.critical(f"🔥 [Watchdog] Fatal Watchdog Monitor Error: {e}")
            await report_error(bot, chat_id, e, context_info="Fatal Watchdog Error")
            await asyncio.sleep(30)  # Warten und nach 30 Sekunden erneut versuchen
