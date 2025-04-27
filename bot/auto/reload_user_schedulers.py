# bot/auto/reload_user_schedulers.py

"""
Reloads all user-specific timezone schedulers after a restart.
Keeps the Bot fully timezone-aware across reboots.
"""

from bot.utils.user_timezone_manager import load_user_timezones
from bot.auto.user_timezone_scheduler import start_user_timezone_scheduler
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

async def reload_all_user_schedulers(application):
    """
    Reloads timezone-specific schedulers for all known users.
    """
    try:
        user_timezones = load_user_timezones()

        if not user_timezones:
            logger.info("🔄 No user timezones found to reload.")
            return

        for chat_id_str, timezone in user_timezones.items():
            chat_id = int(chat_id_str)
            start_user_timezone_scheduler(application, chat_id)

        logger.info(f"✅ Successfully reloaded {len(user_timezones)} user timezone schedulers.")

    except Exception as e:
        logger.error(f"❌ Error reloading user timezone schedulers: {e}")
