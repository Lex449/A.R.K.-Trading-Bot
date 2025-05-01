"""
A.R.K. Auto-Analysis Scheduler – Silent Precision Loop v2.1  
Startet alle 60 Sekunden einen diskreten Marktscan – ohne Spam, nur bei validen Signalen.  
Made in Bali. Engineered with German Precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.auto.auto_analysis import auto_analysis
from bot.utils.logger import setup_logger
from datetime import datetime
import pytz
import asyncio  # <<< CRITICAL!

logger = setup_logger(__name__)

def start_auto_analysis_scheduler(application):
    try:
        scheduler = AsyncIOScheduler(timezone=pytz.utc)
        scheduler.add_job(
            func=lambda: asyncio.create_task(auto_analysis(application)),  # <<< FIXED!
            trigger=IntervalTrigger(seconds=60),
            next_run_time=datetime.utcnow(),
            name="ARK Silent Auto-Analysis"
        )
        scheduler.start()
        logger.info("✅ [Scheduler] Auto-Analysis Scheduler läuft – 60s Loop mit sofortigem Launch.")
    except Exception as e:
        logger.exception("❌ [Scheduler] Fehler beim Starten des Auto-Analysis Schedulers:")
