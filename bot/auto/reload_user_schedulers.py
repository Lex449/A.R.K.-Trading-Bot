"""
Reloads all user-specific timezone schedulers after a restart.
Keeps the Bot fully timezone-aware across reboots.
"""

from bot.utils.user_timezone_manager import load_user_timezones
from bot.auto.user_timezone_scheduler import start_user_timezone_scheduler
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language

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
            # Reload user's timezone-specific scheduler
            start_user_timezone_scheduler(application, chat_id)

            # Fetch the user's language
            lang = get_language(chat_id) or "en"

            # Send confirmation in user's language
            confirmation_message = get_text("timezone_scheduler_reloaded", lang) or "✅ Your timezone-specific scheduler has been successfully reloaded."
            await application.bot.send_message(chat_id, confirmation_message, parse_mode="Markdown")

        logger.info(f"✅ Successfully reloaded {len(user_timezones)} user timezone schedulers.")

    except Exception as e:
        logger.error(f"❌ Error reloading user timezone schedulers: {e}")
        # Error notification in user's language
        error_message = get_text("timezone_scheduler_reload_error", "en") or "❌ There was an error while reloading your timezone-specific scheduler."
        await application.bot.send_message(chat_id, error_message, parse_mode="Markdown")
