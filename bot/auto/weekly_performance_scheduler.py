"""
A.R.K. Weekly Performance Report Scheduler – Full Auto Build
Sends detailed weekly win/loss and performance report every Sunday at 20:00 local user time.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.analytics.win_loss_report import generate_win_loss_report
from bot.utils.logger import setup_logger
from bot.utils.language import get_language
from bot.config.settings import get_settings

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

# Global Scheduler
weekly_performance_scheduler = AsyncIOScheduler()

async def send_weekly_performance_report(application, chat_id: int):
    """
    Sends a detailed win/loss performance report.
    """
    try:
        bot = application.bot
        lang = get_language(chat_id) or "en"

        report_text = generate_win_loss_report(lang)

        await bot.send_message(
            chat_id=chat_id,
            text=report_text,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"✅ [Weekly Performance] Report sent to {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [Weekly Performance Error] {e}")

def start_weekly_performance_scheduler(application, chat_id: int):
    """
    Schedules the Weekly Performance Report every Sunday at 20:00 local time.
    """

    try:
        weekly_performance_scheduler.remove_all_jobs()

        trigger = CronTrigger(
            day_of_week="sun",
            hour=20,
            minute=0,
            timezone="Asia/Singapore"  # Dynamisch pro User später
        )

        weekly_performance_scheduler.add_job(
            send_weekly_performance_report,
            trigger=trigger,
            args=[application, chat_id],
            id="weekly_performance_report",
            replace_existing=True,
            name="Weekly Performance Report Job"
        )

        if not weekly_performance_scheduler.running:
            weekly_performance_scheduler.start()

        logger.info("✅ [Scheduler] Weekly Performance scheduled successfully.")

    except Exception as e:
        logger.error(f"❌ [Scheduler Error] Weekly Performance Scheduler: {e}")
