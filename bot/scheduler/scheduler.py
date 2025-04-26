# bot/scheduler/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.daily_analysis import daily_analysis_job
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def setup_scheduler(application):
    """
    Initializes and schedules all background jobs for the A.R.K. Trading Bot.
    """

    scheduler = AsyncIOScheduler()

    # === Daily Market Analysis Job ===
    scheduler.add_job(
        daily_analysis_job,
        trigger="cron",
        hour=16,
        minute=0,
        timezone="Asia/Makassar",  # Bali time zone (WITA)
        args=[application],
        id="daily_analysis_job",
        name="Daily Advanced Market Analysis"
    )
    logger.info("📊 Daily Analysis Job scheduled at 16:00 Bali time.")

    # === Background Auto Signal Loop ===
    application.create_task(auto_signal_loop())
    logger.info("📈 Auto Signal Loop started as background task.")

    # === Start Scheduler ===
    scheduler.start()
    logger.info("✅ Scheduler initialized and all jobs scheduled successfully.")
