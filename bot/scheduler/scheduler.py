# bot/scheduler/scheduler.py

"""
A.R.K. Ultra Scheduler – 24/7 Marktüberwachung auf Wall Street Niveau.
Strukturiert. Skalierbar. Robust.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.auto.daily_analysis import daily_analysis_job
from bot.utils.logger import setup_logger

# === Logger Setup ===
logger = setup_logger(__name__)

def setup_scheduler(application):
    """
    Initialisiert und plant alle Hintergrundprozesse des A.R.K. Trading Bots:
    - Tägliche Marktanalyse
    - Autonomer Auto Signal Loop
    """

    scheduler = AsyncIOScheduler()

    # === Geplanter Daily Analysis Job ===
    scheduler.add_job(
        func=daily_analysis_job,
        trigger="cron",
        hour=16,
        minute=0,
        timezone="Asia/Makassar",  # Bali Zeit (WITA)
        args=[application],
        id="daily_analysis_job",
        name="Daily Advanced Market Analysis",
        misfire_grace_time=300  # 5 Minuten Kulanzzeit
    )
    logger.info("📊 Daily Analysis Job eingeplant für 16:00 Uhr WITA.")

    # === Autonomer Auto Signal Loop (rund um die Uhr) ===
    application.create_task(auto_signal_loop())
    logger.info("📈 Auto Signal Loop als Hintergrundprozess gestartet.")

    # === Scheduler starten ===
    scheduler.start()
    logger.info("✅ Scheduler vollständig initialisiert und alle Jobs laufen stabil.")
