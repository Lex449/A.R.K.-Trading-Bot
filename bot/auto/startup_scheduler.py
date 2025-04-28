"""
A.R.K. Startup Scheduler – Full Auto Reload Build
Initializes all schedulers and user-specific timezone jobs.
"""

import logging
from bot.auto.daily_scheduler import start_daily_analysis_scheduler
from bot.auto.heartbeat_scheduler import start_heartbeat
from bot.auto.weekly_recap_scheduler import start_weekly_recap_scheduler
from bot.auto.weekly_performance_scheduler import start_weekly_performance_scheduler
from bot.auto.reload_user_scheduler import reload_all_user_schedulers
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup structured logger
logger = setup_logger(__name__)

# Load config
config = get_settings()

async def start_all_schedulers(application):
    """
    Starts all necessary schedulers at bot startup.
    """

    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        # Start core schedulers
        start_daily_analysis_scheduler(application, chat_id)
        start_heartbeat(application, chat_id)

        # Start weekly schedulers
        start_weekly_recap_scheduler(application, chat_id)
        start_weekly_performance_scheduler(application, chat_id)

        # Reload all user timezone-specific schedulers
        await reload_all_user_schedulers(application)

        logger.info("✅ [Startup Scheduler] All schedulers initialized successfully.")

    except Exception as e:
        logger.error(f"❌ [Startup Scheduler Error] {e}")
