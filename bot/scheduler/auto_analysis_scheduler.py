"""
A.R.K. Auto-Analysis Scheduler – Silent Precision Loop v3.1  
Railway-kompatibel. Führt alle 60s einen vollständigen Scan durch.  
Made in Bali. Engineered with German Precision.
"""

import asyncio
from datetime import datetime
import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram.ext import ContextTypes
from bot.auto.auto_analysis import auto_analysis
from bot.utils.logger import setup_logger

logger = setup_logger(__name__)

def start_auto_analysis_scheduler(job_queue):
    try:
        scheduler = AsyncIOScheduler(timezone=pytz.utc)

        # Wrapper für APScheduler-kompatiblen Kontext
        def launch_analysis(context: ContextTypes.DEFAULT_TYPE):
            asyncio.create_task(auto_analysis(context))

        scheduler.add_job(
            func=launch_analysis,
            trigger=IntervalTrigger(seconds=60),
            next_run_time=datetime.utcnow(),
            name="ARK Silent Auto-Analysis"
        )

        scheduler.start()
        logger.info("✅ [Scheduler] Auto-Analysis Scheduler läuft – 60s Loop gestartet.")

    except Exception as e:
        logger.exception("❌ [Scheduler] Fehler beim Starten des Auto-Analysis Schedulers:")
