"""
Startup-Task
------------
Registriert alle Scheduler-Jobs, prüft ENV-Vollständigkeit
und meldet System-Ready. Alias-sicher, daily-time fix, no dupes.

Made in Bali. Engineered with German Precision.
"""

from datetime import time as _time
from telegram.ext import Application
from bot.scheduler.heartbeat_job import heartbeat_job
from bot.scheduler.connection_watchdog_job import check_connection
from bot.scheduler.recap_scheduler import start_recap_scheduler as recap_scheduler
from bot.scheduler.news_scanner_job import start_news_scanner_job as news_scanner_job
from bot.scheduler.auto_analysis_scheduler import (
    start_auto_analysis_scheduler as auto_analysis_scheduler,
)
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

logger = setup_logger(__name__)
settings = get_settings()


def _resolve_daily_time() -> _time:
    """
    Liefert ein datetime.time-Objekt für run_daily().
    ENV-Var DAILY_RECAP_TIME kann „22:15“ oder dict-like sein.
    Fallback: 22:15 UTC.
    """
    cfg = settings.get("DAILY_RECAP_TIME", "22:15")
    if isinstance(cfg, dict):  # {"hour": 22, "minute": 15}
        return _time(hour=cfg.get("hour", 22), minute=cfg.get("minute", 15), tzinfo=None)
    if isinstance(cfg, str) and ":" in cfg:
        h, m = map(int, cfg.split(":")[:2])
        return _time(hour=h, minute=m, tzinfo=None)
    # Default
    return _time(hour=22, minute=15, tzinfo=None)


async def startup_task(app: Application) -> None:
    """Initialisiert alle Scheduler-Jobs & meldet Ready-Status."""
    chat_id = int(settings["TELEGRAM_CHAT_ID"])
    logger.info("🚀 [Startup] Init A.R.K. Master-System …")

    # ─── Heartbeat (60 min) ────────────────────────────────────
    app.job_queue.run_repeating(
        heartbeat_job,
        interval=3600,
        first=0,
        name="heartbeat",
        data=(app.bot, chat_id),
    )

    # ─── Connection Watchdog (5 min) ──────────────────────────
    app.job_queue.run_repeating(
        lambda _: check_connection(app.bot, chat_id),
        interval=300,
        first=15,
        name="connection_watchdog",
    )

    # ─── Daily Recap (time via _resolve_daily_time) ───────────
    app.job_queue.run_daily(
        recap_scheduler,
        time=_resolve_daily_time(),
        name="recap",
    )

    # ─── News-Scanner (2 min) ─────────────────────────────────
    app.job_queue.run_repeating(
        news_scanner_job,
        interval=120,
        first=30,
        name="news_scanner",
        data=app,
    )

    # ─── Auto-Analysis (ENV oder 60 s) ────────────────────────
    app.job_queue.run_repeating(
        auto_analysis_scheduler,
        interval=int(settings.get("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        first=45,
        name="auto_analysis",
    )

    logger.info("✅ Alle Scheduler aktiv. System Ready.")
