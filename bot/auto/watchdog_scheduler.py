# bot/auto/watchdog_scheduler.py

import logging
import time
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings
from bot.utils.connection_watchdog import check_connection
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.utils.error_reporter import report_error

# Logger
logger = setup_logger(__name__)
config = get_settings()

# Scheduler Setup
super_watchdog_scheduler = AsyncIOScheduler()

# Heartbeat Tracking
_last_heartbeat = time.time()

def refresh_heartbeat():
    """Updates the last known healthy heartbeat timestamp."""
    global _last_heartbeat
    _last_heartbeat = time.time()

async def super_watchdog(application, chat_id: int):
    """
    Continuously monitors bot health, auto-signal loop, and Telegram connection.
    """
    bot = application.bot
    logger.info("🛡️ [Super Watchdog] Activated – Maximum Protection Mode.")

    while True:
        try:
            now = time.time()

            # 1. Telegram Connection Check
            is_connected = await check_connection(bot, chat_id)
            if not is_connected:
                logger.error("❌ [Super Watchdog] Lost connection to Telegram API. Retrying...")
                await report_error(bot, chat_id, Exception("Telegram connection lost! Attempting recovery."), context_info="SuperWatchdog Telegram Failure")
                await asyncio.sleep(30)  # Retry after 30 seconds
                continue

            # 2. Signal Loop Crash Detection
            time_since_last_heartbeat = now - _last_heartbeat
            if time_since_last_heartbeat > 90:
                logger.warning("⚠️ [Super Watchdog] No heartbeat detected! Restarting Auto-Signal Loop.")
                await report_error(bot, chat_id, Exception("Auto-Signal Loop stalled, restarting..."), context_info="SuperWatchdog Loop Restart")

                # Restart Auto-Signal Loop
                asyncio.create_task(auto_signal_loop())  # Restart the auto-signal loop
                refresh_heartbeat()  # Reset the heartbeat

            # 3. Optional Status Ping (every 6 hours)
            if now % (6 * 3600) < 30:  # Every 6 hours, send a status ping
                await bot.send_message(
                    chat_id=chat_id,
                    text="✅ *Status Ping:* A.R.K. Bot läuft stabil.",
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
                logger.info("✅ [Super Watchdog] Status ping sent.")

            await asyncio.sleep(30)  # Check every 30 seconds

        except Exception as e:
            logger.critical(f"🔥 [Super Watchdog] Fatal Error: {e}")
            await report_error(bot, chat_id, e, context_info="SuperWatchdog Fatal Error")
            await asyncio.sleep(30)  # Wait and retry after error

def start_super_watchdog(application, chat_id: int):
    """
    Starts the Super Watchdog as a scheduled background task.
    """
    try:
        super_watchdog_scheduler.remove_all_jobs()

        super_watchdog_scheduler.add_job(
            super_watchdog,
            trigger=IntervalTrigger(seconds=30),  # Run every 30 seconds
            args=[application, chat_id],
            id=f"super_watchdog_{chat_id}",
            replace_existing=True,
            name=f"Super Watchdog Monitor for {chat_id}",
            misfire_grace_time=300
        )

        if not super_watchdog_scheduler.running:
            super_watchdog_scheduler.start()

        logger.info(f"✅ [Super Watchdog Scheduler] Fully activated for chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [Super Watchdog Scheduler] Failed to start: {e}")
