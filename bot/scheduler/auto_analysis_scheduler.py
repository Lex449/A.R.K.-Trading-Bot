"""
A.R.K. Auto-Analysis Scheduler – Silent Precision Loop v2.5  
Railway-kompatibel. Führt alle 60s einen vollständigen Scan durch.
Made in Bali. Engineered with German Precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import pytz

from bot.auto.auto_analysis import auto_analysis
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def start_auto_analysis_scheduler(job_queue):
    try:
        scheduler = AsyncIOScheduler(timezone=pytz.utc)

        async def launch_analysis():
            context = job_queue.context  # Wichtiger Fix für Replit / Railway
            await auto_analysis(context)

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
