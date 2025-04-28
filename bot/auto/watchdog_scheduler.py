"""
A.R.K. Watchdog Scheduler – Connection Health Monitoring Layer
Periodically checks the Telegram Bot connection to maximize uptime.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.utils.logger import setup_logger
from bot.utils.connection_watchdog import check_connection
from bot.config.settings import get_settings

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()

# Global Watchdog Scheduler
watchdog_scheduler = AsyncIOScheduler()

def start_watchdog(application, chat_id: int):
    """
    Starts a scheduled Watchdog task to check bot connectivity every 30 minutes.
    """
    try:
        watchdog_scheduler.remove_all_jobs()

        watchdog_scheduler.add_job(
            check_connection,
            trigger=IntervalTrigger(minutes=30),  # Every 30 minutes
            args=[application.bot, chat_id],
            id=f"watchdog_check_{chat_id}",
            replace_existing=True,
            name=f"Telegram Connection Watchdog for {chat_id}",
            misfire_grace_time=300
        )

        if not watchdog_scheduler.running:
            watchdog_scheduler.start()

        logger.info(f"✅ [Watchdog Scheduler] Connection monitoring started for chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [Watchdog Scheduler] Failed to start: {e}")
