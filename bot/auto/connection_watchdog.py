"""
A.R.K. Connection Watchdog – Ultra Defense Layer.
Monitors Telegram Bot connection health and reports critical failures.
"""

from telegram import Bot
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings

# Logger & Config
logger = setup_logger(__name__)
config = get_settings()

async def check_connection(bot: Bot, chat_id: int) -> bool:
    """
    Verifies Telegram Bot API connectivity by calling get_me().
    Returns True if connection is valid, False otherwise.

    Args:
        bot (Bot): Telegram Bot instance.
        chat_id (int): Chat ID for notifications.

    Returns:
        bool: True if connection stable, False if failure detected.
    """
    try:
        await bot.get_me()
        logger.info("✅ [ConnectionWatchdog] Telegram connection verified successfully.")
        return True

    except Exception as e:
        lang = get_language(chat_id)
        warning = get_text("connection_lost", lang)

        logger.error(f"❌ [ConnectionWatchdog] Connection failure: {e}")
        await report_error(bot, chat_id, e, context_info="Telegram Connection Failure")

        try:
            await bot.send_message(
                chat_id=chat_id,
                text=warning,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            logger.warning("⚠️ [ConnectionWatchdog] User notified about Telegram outage.")
        except Exception as alert_error:
            logger.critical(f"🔥 [ConnectionWatchdog] Failed to send alert message: {alert_error}")

        return False
