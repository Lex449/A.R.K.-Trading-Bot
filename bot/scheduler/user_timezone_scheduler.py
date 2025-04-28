"""
A.R.K. User Timezone Scheduler – Ultra Premium Dynamic Scheduling System.
Handles Recap & Reset Jobs automatically for any user based on personal timezone.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.daily_recap_job import daily_recap_job
from bot.auto.weekly_recap_job import weekly_recap_job
from bot.auto.reset_today_job import reset_today_job
from bot.auto.reset_week_job import reset_week_job
from bot.utils.user_timezone_manager import get_user_timezone
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.utils.error_reporter import report_error

# Logger
logger = setup_logger(__name__)

async def start_user_timezone_scheduler(application, chat_id: int):
    """
    Starts personalized background jobs based on user timezone.
    Includes Daily Recap, Weekly Recap, Daily Reset, Weekly Reset.
    """

    try:
        timezone = get_user_timezone(chat_id)
        scheduler = AsyncIOScheduler(timezone=timezone)

        # === Daily Recap (Personalized Timezone) ===
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

        # === Weekly Recap (Friday) ===
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

        # === Daily Reset (Midnight) ===
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

        # === Weekly Reset (Monday) ===
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
        logger.info(f"✅ User-Specific Scheduler started for {chat_id} (Timezone: {timezone}).")

    except Exception as e:
        logger.error(f"❌ [Scheduler Error] Could not setup user scheduler for {chat_id}: {e}")
        await report_error(application.bot, chat_id, e, context_info="User Timezone Scheduler Failure")
        try:
            await application.bot.send_message(
                chat_id=chat_id,
                text=get_text("scheduler_error", get_language(chat_id)) or "⚠️ Scheduler setup failed. Please try again.",
                parse_mode="Markdown"
            )
        except Exception as inner_error:
            logger.error(f"❌ [Scheduler Alert Error] Failed to notify user {chat_id}: {inner_error}")
