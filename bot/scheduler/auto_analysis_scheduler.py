"""
A.R.K. Auto-Analysis Scheduler – Silent Precision Loop v2.0  
Startet alle 60 Sekunden einen diskreten Marktscan – ohne Spam, nur bei relevanten Signalen.  
Maximiert API-Auslastung ohne Telegram-Clutter.  
Made in Bali. Engineered with German Precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.auto.auto_analysis import auto_analysis
from bot.utils.logger import setup_logger
from datetime import datetime
import pytz

logger = setup_logger(__name__)

def start_auto_analysis_scheduler(application):
    try:
        scheduler = AsyncIOScheduler(timezone=pytz.utc)
        scheduler.add_job(
            func=lambda: auto_analysis(application),
            trigger=IntervalTrigger(seconds=60),
            next_run_time=datetime.utcnow(),  # Sofortiger Start
            name="ARK Silent Auto-Analysis"
        )
        scheduler.start()
        logger.info("✅ [Scheduler] Auto-Analysis Scheduler aktiviert – 60s Loop mit sofortigem Launch.")
    except Exception as e:
        logger.exception("❌ [Scheduler] Fehler beim Start des Auto-Analysis Schedulers:")
