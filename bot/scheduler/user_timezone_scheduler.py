"""
A.R.K. User Timezone Scheduler – Handles dynamic Recap & Reset Jobs per user timezone.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.daily_recap_job import daily_recap_job
from bot.auto.weekly_recap_job import weekly_recap_job
from bot.auto.reset_today_job import reset_today_job
from bot.auto.reset_week_job import reset_week_job
from bot.utils.user_timezone_manager import get_user_timezone
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

def start_user_timezone_scheduler(application, chat_id: int):
    """
    Launches personalized background jobs for each user based on timezone.
    """

    timezone = get_user_timezone(chat_id)
    scheduler = AsyncIOScheduler(timezone=timezone)

    # Daily Recap (custom timezone)
    scheduler.add_job(
        func=daily_recap_job,
        trigger="cron",
        hour=16,
        minute=5,
        args=[application, chat_id],
        id=f"daily_recap_{chat_id}",
        name=f"Daily Recap for {chat_id}",
        misfire_grace_time=300
    )
    logger.info(f"📊 Daily Recap scheduled for {chat_id} at 16:05 ({timezone}).")

    # Weekly Recap (Friday)
    scheduler.add_job(
        func=weekly_recap_job,
        trigger="cron",
        day_of_week="fri",
        hour=16,
        minute=10,
        args=[application, chat_id],
        id=f"weekly_recap_{chat_id}",
        name=f"Weekly Recap for {chat_id}",
        misfire_grace_time=600
    )
    logger.info(f"📈 Weekly Recap scheduled for {chat_id} (Friday 16:10 {timezone}).")

    # Daily Reset
    scheduler.add_job(
        func=reset_today_job,
        trigger="cron",
        hour=23,
        minute=59,
        args=[chat_id],
        id=f"reset_today_{chat_id}",
        name=f"Daily Reset for {chat_id}",
        misfire_grace_time=300
    )
    logger.info(f"♻️ Daily Reset scheduled for {chat_id} at 23:59 ({timezone}).")

    # Weekly Reset
    scheduler.add_job(
        func=reset_week_job,
        trigger="cron",
        day_of_week="mon",
        hour=0,
        minute=0,
        args=[chat_id],
        id=f"reset_week_{chat_id}",
        name=f"Weekly Reset for {chat_id}",
        misfire_grace_time=600
    )
    logger.info(f"♻️ Weekly Reset scheduled for {chat_id} (Monday 00:00 {timezone}).")

    scheduler.start()
    logger.info(f"✅ Scheduler started for user {chat_id} (Timezone: {timezone}).")
