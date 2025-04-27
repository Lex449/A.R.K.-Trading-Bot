"""
A.R.K. Ultra Scheduler – Full 24/7 Operation.
Manages Auto-Signals, Recaps, and Reset Jobs seamlessly.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.daily_recap_job import daily_recap_job
from bot.auto.weekly_recap_job import weekly_recap_job
from bot.auto.reset_today_job import reset_today_job
from bot.auto.reset_week_job import reset_week_job
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

def setup_scheduler(application):
    """
    Schedules all background operations for A.R.K.:
    - Auto Signal Loop
    - Daily Recap + Reset
    - Weekly Recap + Reset
    """

    scheduler = AsyncIOScheduler()

    # === Continuous Auto Signal Loop (non-blocking) ===
    application.create_task(auto_signal_loop())
    logger.info("🚀 Auto Signal Loop launched as background task.")

    # === Scheduled Daily Recap (16:05 WITA) ===
    scheduler.add_job(
        daily_recap_job,
        trigger="cron",
        hour=16,
        minute=5,
        timezone="Asia/Makassar",
        args=[application],
        id="daily_recap_job",
        name="Daily Recap Job",
        misfire_grace_time=300
    )
    logger.info("📊 Daily Recap Job scheduled (16:05 WITA).")

    # === Scheduled Weekly Recap (Friday 16:10 WITA) ===
    scheduler.add_job(
        weekly_recap_job,
        trigger="cron",
        day_of_week="fri",
        hour=16,
        minute=10,
        timezone="Asia/Makassar",
        args=[application],
        id="weekly_recap_job",
        name="Weekly Recap Job",
        misfire_grace_time=600
    )
    logger.info("📈 Weekly Recap Job scheduled (Friday 16:10 WITA).")

    # === Daily Session Data Reset (23:59 WITA) ===
    scheduler.add_job(
        reset_today_job,
        trigger="cron",
        hour=23,
        minute=59,
        timezone="Asia/Makassar",
        id="reset_today_job",
        name="Reset Today Job",
        misfire_grace_time=300
    )
    logger.info("♻️ Daily Reset Job scheduled (23:59 WITA).")

    # === Weekly Session Data Reset (Monday 00:00 WITA) ===
    scheduler.add_job(
        reset_week_job,
        trigger="cron",
        day_of_week="mon",
        hour=0,
        minute=0,
        timezone="Asia/Makassar",
        id="reset_week_job",
        name="Reset Week Job",
        misfire_grace_time=600
    )
    logger.info("♻️ Weekly Reset Job scheduled (Monday 00:00 WITA).")

    # === Start the scheduler ===
    scheduler.start()
    logger.info("✅ Ultra Scheduler fully initialized and running.")
