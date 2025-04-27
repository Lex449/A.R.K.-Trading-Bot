"""
Global Scheduler – Manages continuous Auto-Signal Loop.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from bot.auto.auto_signal_loop import auto_signal_loop
from bot.utils.logger import setup_logger

# Logger
logger = setup_logger(__name__)

def start_global_scheduler(application):
    """
    Launches continuous background processes that do not depend on timezones.
    """

    scheduler = AsyncIOScheduler()

    # === Auto Signal Loop (continuous) ===
    application.create_task(auto_signal_loop())
    logger.info("🚀 Auto Signal Loop launched.")

    # === Start Scheduler ===
    scheduler.start()
    logger.info("✅ Global Scheduler running (Auto Signal only).")
