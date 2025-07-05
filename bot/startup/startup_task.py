"""
Start-Up-Routine: prüft ENV, setzt Scheduler-Jobs, pingt System-Status.
"""

from telegram.ext import Application
from bot.scheduler.heartbeat_job import heartbeat_job
from bot.scheduler.connection_watchdog_job import check_connection
from bot.scheduler.recap_scheduler import recap_scheduler
from bot.scheduler.news_scanner_job import news_scanner_job
from bot.scheduler.auto_analysis_scheduler import auto_analysis_scheduler
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

logger   = setup_logger(__name__)
settings = get_settings()


async def startup_task(application: Application) -> None:
    """Initialisiert alle Hintergrund-Jobs & sendet Startup-Ping."""
    chat_id = int(settings["TELEGRAM_CHAT_ID"])

    logger.info("🚀 [Startup] Initialisiere A.R.K. Master-System...")

    # 1) Heartbeat (jede Stunde)
    application.job_queue.run_repeating(
        heartbeat_job, interval=3600, first=0, name="heartbeat", data=chat_id
    )
    logger.info("✅ [Startup] Heartbeat aktiviert.")

    # 2) Connection-Watchdog (alle 5 Min.)
    application.job_queue.run_repeating(
        lambda _: check_connection(application.bot, chat_id),
        interval=300,
        first=10,
        name="connection_watchdog",
    )
    logger.info("✅ [Startup] Connection Watchdog aktiviert.")

    # 3) Recap Scheduler (22:15 UTC täglich)
    application.job_queue.run_daily(
        recap_scheduler, time=dict(hour=22, minute=15, tzinfo="UTC"), name="recap"
    )
    logger.info("✅ [Startup] Recap Scheduler aktiviert.")

    # 4) News-Scanner (alle 2 Min. während US-Session)
    application.job_queue.run_repeating(
        news_scanner_job,
        interval=120,
        first=20,
        name="news_scanner",
        data=application,
    )

    # 5) Auto-Analysis Loop (alle 60 Sek.)
    application.job_queue.run_repeating(
        auto_analysis_scheduler,
        interval=int(settings.get("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        first=30,
        name="auto_analysis",
    )

    logger.info("✅ [Startup] Alle Scheduler aktiviert.")
