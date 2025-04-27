# bot/auto/scheduler.py

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.daily_analysis import daily_analysis_job
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def setup_scheduler(application):
    """
    Initialisiert den AsyncIO Scheduler für geplante Aufgaben:
    - Tägliche Analyse-Reports (daily_analysis_job)
    - Kontinuierlicher Auto Signal Loop (auto_signal_loop)
    """
    scheduler = AsyncIOScheduler()

    # === Scheduled Daily Analysis ===
    scheduler.add_job(
        func=daily_analysis_job,
        trigger="cron",
        hour=16,
        minute=0,
        timezone="Asia/Makassar",  # Bali Zeit (WITA)
        args=[application],
        id="daily_analysis_job",
        misfire_grace_time=300  # 5 Minuten Kulanz bei Verpassen
    )
    logger.info("[Scheduler] Daily Analysis Job für 16:00 WITA eingeplant.")

    # === Start Continuous Auto Signal Loop ===
    application.create_task(auto_signal_loop())
    logger.info("[Scheduler] Auto Signal Loop gestartet.")

    # === Start Scheduler ===
    scheduler.start()
    logger.info("[Scheduler] AsyncIO Scheduler erfolgreich gestartet.")
