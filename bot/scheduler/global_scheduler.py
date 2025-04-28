"""
Global Scheduler – Manages continuous Auto-Signal Loop.
Ensures uninterrupted, real-time signal detection and execution.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Logger
logger = setup_logger(__name__)

def start_global_scheduler(application):
    """
    Launches continuous background processes that do not depend on timezones.
    """

    try:
        scheduler = AsyncIOScheduler()

        # === Auto Signal Loop (continuous) ===
        application.create_task(auto_signal_loop())
        logger.info("🚀 Auto Signal Loop launched successfully.")

        # === Start Scheduler ===
        scheduler.start()
        logger.info("✅ Global Scheduler running (Auto Signal Loop is active).")
    
    except Exception as e:
        # If an error occurs while starting the scheduler or Auto Signal loop, log it
        logger.error(f"❌ Failed to start Global Scheduler: {e}")
        # Send the error report to the admin
        await report_error(application.bot, application.bot.id, e, context_info="Global Scheduler Error")
