# bot/auto/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.daily_analysis import daily_analysis_job
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def setup_scheduler(application):
    """
    Sets up the AsyncIO Scheduler for the bot to run scheduled tasks cleanly.
    Includes Daily Analysis Jobs and the continuous Auto Signal Loop.
    """
    scheduler = AsyncIOScheduler()

    # === Scheduled Daily Analysis (every trading day) ===
    scheduler.add_job(
        daily_analysis_job,
        trigger="cron",
        hour=16,
        minute=0,
        timezone="Asia/Makassar",  # Bali time (WITA)
        args=[application],
        id="daily_analysis_job",
        misfire_grace_time=300  # 5 Minuten Puffer falls Job verpasst
    )
    logger.info("[Scheduler] Daily Analysis job scheduled for 16:00 WITA.")

    # === Continuous Auto Signal Loop (infinite task) ===
    application.create_task(auto_signal_loop())
    logger.info("[Scheduler] Auto Signal Loop task started.")

    # === Start Scheduler ===
    scheduler.start()
    logger.info("[Scheduler] AsyncIO Scheduler started successfully.")
