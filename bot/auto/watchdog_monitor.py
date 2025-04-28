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
            # Hole den letzten Heartbeat-Zeitstempel aus der Watchdog State
            last_heartbeat = get_last_heartbeat()
            time_since_last_heartbeat = time.time() - last_heartbeat

            # Überprüfe, ob der Auto-Signal-Loop abgestürzt ist (keine Heartbeats innerhalb von 90 Sekunden)
            if time_since_last_heartbeat > 90:
                logger.critical("⚠️ [Watchdog] Auto-Signal Loop heartbeat missing! Restart triggered.")
                # Fehlerbericht senden, dass der Auto-Signal-Loop abgestürzt ist
                await report_error(bot, chat_id, Exception("Auto-Signal Loop crashed. Restarting..."), context_info="Watchdog Crash Detection")

                # Importiere und starte den Auto-Signal-Loop nur im Fehlerfall (Lazy Import)
                from bot.auto.auto_signal_loop import auto_signal_loop
                asyncio.create_task(auto_signal_loop())  # Neustart des Auto-Signal-Loops

            await asyncio.sleep(30)  # Warte 30 Sekunden, bevor die nächste Überprüfung erfolgt

        except Exception as e:
            # Logge und melde Fehler im Watchdog-Monitor
            logger.critical(f"🔥 [Watchdog] Fatal Watchdog Monitor Error: {e}")
            await report_error(bot, chat_id, e, context_info="Fatal Watchdog Error")
            await asyncio.sleep(30)  # Warte 30 Sekunden, bevor erneut überprüft wird
