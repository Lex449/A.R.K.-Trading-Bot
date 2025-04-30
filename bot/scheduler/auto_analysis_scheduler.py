"""
A.R.K. Auto-Analysis Scheduler – Silent Loop Edition
Startet alle 60 Sekunden einen vollständigen Markt-Scan – nur mit Signal-Output.
Made in Bali. Engineered with German Precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_analysis import auto_analysis
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def start_auto_analysis_scheduler(application):
    try:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(lambda: auto_analysis(application), "interval", seconds=60)
        scheduler.start()
        logger.info("✅ [Scheduler] Auto-Analysis Scheduler gestartet.")
    except Exception as e:
        logger.error(f"❌ [Scheduler] Fehler beim Start des Auto-Analysis Schedulers: {e}")
