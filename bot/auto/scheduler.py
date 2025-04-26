# bot/auto/scheduler.py

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.auto.auto_signal import auto_signal_loop
from bot.auto.auto_analysis import daily_analysis_job

# Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def start_scheduler(app):
    """
    Starts the trading signal scheduler and daily analysis scheduler.
    """

    scheduler = AsyncIOScheduler()

    # Auto Signal Loop (läuft permanent im Hintergrund)
    app.create_task(auto_signal_loop())

    # Daily Analysis Job – jeden Handelstag 30 Minuten vor US-Börsenstart
    scheduler.add_job(
        daily_analysis_job,
        CronTrigger(hour=9, minute=0, timezone="America/New_York"),  # 09:00 NY Time (vor 09:30 NYSE-Opening)
        args=(app.bot,),
        name="Daily Market Analysis Job"
    )

    scheduler.start()
    logger.info("✅ Scheduler gestartet: Auto-Signale & tägliche Analyse aktiviert.")
