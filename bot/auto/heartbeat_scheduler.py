# bot/auto/heartbeat_scheduler.py

"""
A.R.K. Heartbeat Scheduler – Daily Analysis Auto-Recovery.
Ensures Daily Scheduler is always active.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.auto.daily_scheduler import daily_scheduler, start_daily_analysis_scheduler
from bot.utils.logger import setup_logger

# Logger Setup
logger = setup_logger(__name__)

# Heartbeat Scheduler (separat vom normalen Scheduler)
heartbeat_scheduler = AsyncIOScheduler()

def start_heartbeat(application):
    """
    Starts the Heartbeat Monitoring to ensure Daily Scheduler stays alive.
    """
    try:
        # Alle alten Jobs entfernen (Safety)
        heartbeat_scheduler.remove_all_jobs()

        # Heartbeat alle 5 Minuten
        heartbeat_scheduler.add_job(
            check_daily_scheduler,
            trigger=IntervalTrigger(minutes=5),
            args=[application],
            id="heartbeat_check_daily",
            replace_existing=True,
            name="Heartbeat – Check Daily Scheduler"
        )

        heartbeat_scheduler.start()

        logger.info("✅ [Heartbeat] Daily Scheduler Heartbeat started successfully.")

    except Exception as e:
        logger.error(f"❌ [Heartbeat] Failed to start Heartbeat: {e}")

async def check_daily_scheduler(application):
    """
    Checks if Daily Scheduler is running and restarts if needed.
    """
    if not daily_scheduler.running:
        logger.warning("❗ [Heartbeat] Daily Scheduler is NOT running. Restarting...")
        start_daily_analysis_scheduler(application)
    else:
        logger.info("✅ [Heartbeat] Daily Scheduler is healthy.")
