"""
A.R.K. Weekly Recap Scheduler – Full Auto Build
Sends weekly trading recap every Friday at 20:00 local user time.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.auto.weekly_recap_job import weekly_recap_job
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Global Scheduler
weekly_recap_scheduler = AsyncIOScheduler()

def start_weekly_recap_scheduler(application, chat_id: int):
    """
    Schedules the Weekly Recap every Friday at 20:00 local time.
    """

    try:
        weekly_recap_scheduler.remove_all_jobs()

        trigger = CronTrigger(
            day_of_week="fri",
            hour=20,
            minute=0,
            timezone="Asia/Singapore"  # Dynamisch pro User machbar (später)
        )

        weekly_recap_scheduler.add_job(
            weekly_recap_job,
            trigger=trigger,
            args=[application, chat_id],
            id="weekly_recap",
            replace_existing=True,
            name="Weekly Recap Job"
        )

        if not weekly_recap_scheduler.running:
            weekly_recap_scheduler.start()

        logger.info("✅ [Scheduler] Weekly Recap scheduled successfully.")

    except Exception as e:
        logger.error(f"❌ [Scheduler Error] Weekly Recap Scheduler: {e}")
