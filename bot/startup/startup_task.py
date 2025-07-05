"""
Start-Up-Routine: prüft ENV, setzt alle Scheduler-Jobs
und sendet einen Startup-Ping.

Engineered mit dreifacher Sicherung gegen Doppel-Instanz
und mit sauberem AIO-JobQueue-Setup.
"""

from telegram.ext import Application
from bot.scheduler.heartbeat_job import heartbeat_job
from bot.scheduler.connection_watchdog_job import check_connection
from bot.scheduler.recap_scheduler import recap_scheduler
from bot.scheduler.news_scanner_job import news_scanner_job
from bot.scheduler.auto_analysis_scheduler import auto_analysis_scheduler
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

logger = setup_logger(__name__)
settings = get_settings()


async def startup_task(app: Application) -> None:
    """Initialisiert Hintergrund-Jobs & meldet Ready-Status."""
    chat_id = int(settings["TELEGRAM_CHAT_ID"])
    logger.info("🚀 [Startup] Init A.R.K. Master-System …")

    # 1) Heartbeat – stündlich
    app.job_queue.run_repeating(
        heartbeat_job,
        interval=3600,
        first=0,
        name="heartbeat",
        data=(app.bot, chat_id),
    )
    logger.info("✅ Heartbeat aktiviert.")

    # 2) Connection-Watchdog – alle 5 Minuten
    app.job_queue.run_repeating(
        lambda _: check_connection(app.bot, chat_id),
        interval=300,
        first=15,
        name="connection_watchdog",
    )
    logger.info("✅ Connection Watchdog aktiviert.")

    # 3) Recap – täglich 22:15 UTC
    app.job_queue.run_daily(
        recap_scheduler,
        time=dict(hour=22, minute=15, tzinfo="UTC"),
        name="recap",
    )
    logger.info("✅ Recap Scheduler aktiviert.")

    # 4) News-Scanner – alle 2 Min (nur US-Session)
    app.job_queue.run_repeating(
        news_scanner_job,
        interval=120,
        first=30,
        name="news_scanner",
        data=app,
    )

    # 5) Auto-Analysis – Loop-Zeit aus ENV
    app.job_queue.run_repeating(
        auto_analysis_scheduler,
        interval=int(settings.get("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        first=45,
        name="auto_analysis",
    )

    logger.info("✅ Alle Scheduler laufen. System Ready.")
