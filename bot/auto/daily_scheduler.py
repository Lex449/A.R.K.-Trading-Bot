"""
A.R.K. Daily Scheduler – Hyper Precision Timing System
Automatically triggers the Daily Market Analysis at optimal times.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.auto.daily_analysis_job import daily_analysis_job
from bot.utils.logger import setup_logger

# Logger Setup
logger = setup_logger(__name__)

# Global Scheduler Instance
daily_scheduler = AsyncIOScheduler()

def start_daily_analysis_scheduler(application):
    """
    Starts the Daily Market Analysis once per day at market open.
    """

    try:
        # Trigger exakt zur Markteröffnung
        trigger = CronTrigger(hour=15, minute=0, timezone="Asia/Singapore")  # 15:00 Bali-Zeit = 09:00 CET Frankfurt

        # Sicherheit: Bestehende Jobs entfernen
        daily_scheduler.remove_all_jobs()

        # Daily Job registrieren
        daily_scheduler.add_job(
            daily_analysis_job,
            trigger=trigger,
            args=[application],
            id="daily_market_analysis",
            replace_existing=True,
            name="Daily Market Analysis"
        )

        # Scheduler starten
        if not daily_scheduler.running:
            daily_scheduler.start()

        logger.info("✅ [DailyScheduler] Daily Market Analysis Job scheduled successfully at 15:00 WITA.")

    except Exception as e:
        logger.error(f"❌ [DailyScheduler Error] Failed to start daily scheduler: {e}")
