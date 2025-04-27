"""
A.R.K. Ultra Scheduler – 24/7 Market Surveillance on Wall Street Level.
Fully structured, scalable, and built for precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.daily_recap_job import daily_recap_job
from bot.auto.weekly_recap_job import weekly_recap_job
from bot.utils.logger import setup_logger

# === Logger Setup ===
logger = setup_logger(__name__)

def setup_scheduler(application):
    """
    Initializes and schedules all background jobs for the A.R.K. Trading Bot:
    - Daily Recap (End of day summary)
    - Weekly Recap (Weekly performance & motivation)
    - Continuous Auto-Signal Loop (live market scanning)
    """

    scheduler = AsyncIOScheduler()

    # === Daily Recap Job (Every trading day at 16:05 WITA) ===
    scheduler.add_job(
        func=daily_recap_job,
        trigger="cron",
        hour=16,
        minute=5,
        timezone="Asia/Makassar",  # Bali Time Zone (WITA)
        args=[application],
        id="daily_recap_job",
        name="Daily Recap Job",
        misfire_grace_time=300
    )
    logger.info("📊 Daily Recap Job scheduled at 16:05 WITA.")

    # === Weekly Recap Job (Every Friday at 16:10 WITA) ===
    scheduler.add_job(
        func=weekly_recap_job,
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
    logger.info("📈 Weekly Recap Job scheduled every Friday at 16:10 WITA.")

    # === Continuous Auto Signal Loop ===
    application.create_task(auto_signal_loop())
    logger.info("🚀 Auto Signal Loop started as continuous background task.")

    # === Start Scheduler ===
    scheduler.start()
    logger.info("✅ Ultra Scheduler successfully initialized and running.")
