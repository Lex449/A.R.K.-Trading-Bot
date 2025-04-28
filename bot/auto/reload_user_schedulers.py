"""
A.R.K. Reload User Scheduler
– Ultra Stable Timezone Manager.
– Ensures timezone-specific tasks stay active after restart.
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
    Reloads timezone-specific schedulers for all known users after a bot restart.
    Guarantees 100% uptime for personalized notifications.
    """
    try:
        user_timezones = load_user_timezones()

        if not user_timezones:
            logger.info("🔄 [ReloadScheduler] No user timezones found. Skipping reload.")
            return

        reload_count = 0

        for chat_id_str, timezone in user_timezones.items():
            try:
                chat_id = int(chat_id_str)

                # Start user's timezone-specific scheduler
                start_user_timezone_scheduler(application, chat_id)

                lang = get_language(chat_id) or "en"
                confirmation_message = get_text("timezone_scheduler_reloaded", lang) or "✅ Your timezone-specific scheduler has been reloaded successfully."

                await application.bot.send_message(
                    chat_id=chat_id,
                    text=confirmation_message,
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )

                reload_count += 1

            except Exception as user_error:
                logger.warning(f"⚠️ [ReloadScheduler] Failed for chat_id {chat_id_str}: {user_error}")

        logger.info(f"✅ [ReloadScheduler] Successfully reloaded {reload_count} user timezone schedulers.")

    except Exception as global_error:
        logger.error(f"❌ [ReloadScheduler] Critical error during user scheduler reload: {global_error}")
