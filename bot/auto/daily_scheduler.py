# bot/auto/daily_scheduler.py

"""
A.R.K. Dynamic Daily Scheduler – User-Based Timezone Precision
Schedules Daily Analysis exactly at the user's market open time.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.auto.daily_analysis_job import daily_analysis_job
from bot.utils.user_timezone_manager import get_user_timezone
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

# Global Scheduler
daily_scheduler = AsyncIOScheduler()

def start_daily_analysis_scheduler(application, chat_id: int):
    """
    Schedules the Daily Analysis for a specific user based on their timezone.
    """
    try:
        # Get user's timezone
        user_timezone = get_user_timezone(chat_id)
        if not user_timezone:
            logger.warning(f"⚠️ [Scheduler] No timezone set for chat ID {chat_id}. Using UTC as fallback.")
            user_timezone = "UTC"

        # Define market open time (adjust if needed per user)
        trigger = CronTrigger(hour=9, minute=0, timezone=user_timezone)

        # Remove existing job if exists
        try:
            daily_scheduler.remove_job(job_id=f"daily_analysis_{chat_id}")
        except Exception:
            pass  # Ignore if job doesn't exist yet

        # Add new job
        daily_scheduler.add_job(
            daily_analysis_job,
            trigger=trigger,
            args=[application],
            id=f"daily_analysis_{chat_id}",
            replace_existing=True,
            name=f"Daily Analysis for {chat_id}"
        )

        if not daily_scheduler.running:
            daily_scheduler.start()

        logger.info(f"✅ [Scheduler] Daily Analysis scheduled for {chat_id} at 9:00 {user_timezone}.")

    except Exception as e:
        logger.error(f"❌ [Scheduler Error] Failed to start Daily Analysis for {chat_id}: {e}")
