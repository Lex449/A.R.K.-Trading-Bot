"""
A.R.K. Connection Watchdog – Ultra Defense Layer 2.0
Monitors Telegram Bot connection health and auto-notifies on disruptions.

Built for: Uptime Stability, Alert Resilience, and Fail-Fast Behavior.
Made in Bali. Engineered with German Precision.
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
    Verifies Telegram Bot API connectivity via get_me().
    Auto-notifies user and logs incident if failed.

    Args:
        bot (Bot): Telegram Bot instance
        chat_id (int): Chat ID for alert fallback

    Returns:
        bool: True if connection is stable, False otherwise
    """
    try:
        me = await bot.get_me()
        if me:
            logger.info("✅ [ConnectionWatchdog] Telegram connection verified.")
            return True

        logger.warning("⚠️ [ConnectionWatchdog] Bot returned None on get_me() check.")
        return False

    except Exception as e:
        lang = get_language(chat_id)
        warning = get_text("connection_lost", lang)

        logger.error(f"❌ [ConnectionWatchdog] Telegram connectivity failure: {e}")
        await report_error(bot, chat_id, e, context_info="Telegram API Connection Error")

        try:
            await bot.send_message(
                chat_id=chat_id,
                text=warning,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            logger.warning("⚠️ [ConnectionWatchdog] Alert message sent to user.")
        except Exception as alert_error:
            logger.critical(f"🔥 [ConnectionWatchdog] Alert delivery failed: {alert_error}")

        return False
