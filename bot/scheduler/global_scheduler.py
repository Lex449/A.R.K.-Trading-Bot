"""
A.R.K. Global Scheduler – Master Signal Loop Manager Ultra 2025.
Manages and monitors Auto-Signal Loop for uninterrupted real-time trading signals.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

def start_global_scheduler(application):
    """
    Starts all continuous background monitoring services
    (Signal Loops, Auto-Tasks) with full fault-tolerance.
    """

    try:
        # === Initialize Async Scheduler ===
        scheduler = AsyncIOScheduler()

        # === Start Auto-Signal Loop Task ===
        application.create_task(auto_signal_loop())
        logger.info("🚀 [GlobalScheduler] Auto-Signal Loop initialized successfully.")

        # === Start APScheduler (for future tasks if needed) ===
        scheduler.start()
        logger.info("✅ [GlobalScheduler] APScheduler service started successfully.")

    except Exception as e:
        logger.critical(f"🔥 [GlobalScheduler] FATAL ERROR: {e}")
        try:
            # Critical fallback: attempt error reporting
            application.create_task(report_error(application.bot, application.bot.id, e, context_info="Global Scheduler Critical Startup Error"))
        except Exception as inner_error:
            logger.error(f"⚠️ [GlobalScheduler] Failed to report error: {inner_error}")
