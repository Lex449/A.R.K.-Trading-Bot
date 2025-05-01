"""
A.R.K. Auto-Analysis Scheduler – Silent Precision Loop v3.0  
Kompatibel mit Railway & PTB 20+. Führt alle 60s einen vollständigen Scan durch.  
Made in Bali. Engineered with German Precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import pytz

from bot.auto.auto_analysis import auto_analysis
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def start_auto_analysis_scheduler(application):
    """
    Startet den Auto-Analysis Scheduler mit Zugriff auf den Telegram-Bot-Kontext.
    """
    try:
        scheduler = AsyncIOScheduler(timezone=pytz.utc)

        async def launch_analysis():
            await auto_analysis(application)  # Direkt die Application weiterreichen

        scheduler.add_job(
            func=launch_analysis,
            trigger=IntervalTrigger(seconds=60),
            next_run_time=datetime.utcnow(),
            name="ARK Auto-Analysis 60s"
        )

        scheduler.start()
        logger.info("✅ [Scheduler] Auto-Analysis Scheduler läuft – 60s Loop aktiviert.")

    except Exception as e:
        logger.exception("❌ [Scheduler] Fehler beim Starten des Auto-Analysis Schedulers:")
