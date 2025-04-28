"""
A.R.K. Daily Scheduler – Hyper Precision Timing
Starts Daily Analysis automatically at market open.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.auto.daily_analysis_job import daily_analysis_job
from bot.utils.logger import setup_logger
from bot.utils.user_timezone_manager import get_user_timezone

# Setup Logger
logger = setup_logger(__name__)

# Global Scheduler Instance
daily_scheduler = AsyncIOScheduler()

def start_daily_analysis_scheduler(application, chat_id: int):
    """
    Starts the Daily Analysis for a specific user at their configured market opening.
    """
    try:
        # Load user timezone
        timezone = get_user_timezone(chat_id)

        # Example: Daily at 15:00 (timezone-dependent)
        trigger = CronTrigger(hour=15, minute=0, timezone=timezone)

        daily_scheduler.remove_all_jobs()

        daily_scheduler.add_job(
            daily_analysis_job,
            trigger=trigger,
            args=[application],
            id=f"daily_market_analysis_{chat_id}",
            replace_existing=True,
            name=f"Daily Market Analysis for Chat {chat_id}"
        )

        if not daily_scheduler.running:
            daily_scheduler.start()

        logger.info(f"✅ [Scheduler] Daily Analysis Job scheduled for chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [Scheduler Error] Failed to start daily analysis scheduler: {e}")
