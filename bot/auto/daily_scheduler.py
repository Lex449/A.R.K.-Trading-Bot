# bot/auto/daily_scheduler.py

"""
A.R.K. Daily Scheduler – Full-Symbol Daily Scanner Activation.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.utils.logger import setup_logger
from bot.auto.daily_analysis_job import daily_analysis_job

# Logger Setup
logger = setup_logger(__name__)

daily_scheduler = AsyncIOScheduler()

def start_daily_analysis_scheduler(application, chat_id: int):
    """
    Starts a scheduled daily analysis scan.
    """
    try:
        daily_scheduler.remove_all_jobs()

        daily_scheduler.add_job(
            daily_analysis_job,
            trigger=CronTrigger(hour=9, minute=30),  # NYSE Start (angepasst)
            args=[application],
            id=f"daily_analysis_{chat_id}",
            replace_existing=True,
            name=f"Daily Analysis Job for Chat {chat_id}",
            misfire_grace_time=300
        )

        if not daily_scheduler.running:
            daily_scheduler.start()

        logger.info(f"✅ [DailyScheduler] Daily analysis job scheduled for chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [DailyScheduler] Failed to start Daily Scheduler: {e}")
