"""
A.R.K. Scheduler – Connection Watchdog Monitor 2025
Permanently monitors Telegram API connectivity. Immediate alerts if unstable.
Made in Bali. Engineered with German Precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram import Bot
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# Setup structured logger and settings
logger = setup_logger(__name__)
config = get_settings()

# Initialize global scheduler
watchdog_scheduler = AsyncIOScheduler()

async def check_connection(bot: Bot, chat_id: int):
    """
    Verifies Telegram Bot API connection health.

    Args:
        bot (Bot): Telegram bot instance.
        chat_id (int): Target chat ID for alert reporting.
    """
    try:
        await bot.get_me()
        logger.info(f"✅ [WatchdogJob] Telegram connection healthy.")

    except Exception as e:
        logger.error(f"❌ [WatchdogJob] Connection failure detected: {e}")

        # Try to notify Admin
        try:
            await bot.send_message(
                chat_id=chat_id,
                text="⚠️ *A.R.K. Alert:* Telegram connection temporarily lost. Recovery in progress.",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            logger.info("✅ [WatchdogJob] Warning message sent to Admin.")

        except Exception as alert_error:
            logger.critical(f"🔥 [WatchdogJob] Failed to send connection alert: {alert_error}")

        # Report via error reporter
        await report_error(bot, chat_id, e, context_info="Connection Watchdog Failure")

def start_connection_watchdog(bot: Bot, chat_id: int):
    """
    Starts the connection watchdog to run every 30 minutes.

    Args:
        bot (Bot): Telegram bot instance.
        chat_id (int): Target chat ID.
    """
    try:
        watchdog_scheduler.remove_all_jobs()

        watchdog_scheduler.add_job(
            check_connection,
            trigger=IntervalTrigger(minutes=30),
            args=[bot, chat_id],
            id=f"connection_watchdog_job_{chat_id}",
            replace_existing=True,
            name=f"A.R.K. Connection Watchdog for Chat {chat_id}",
            misfire_grace_time=300
        )

        if not watchdog_scheduler.running:
            watchdog_scheduler.start()

        logger.info(f"✅ [WatchdogJob] Scheduler started for chat_id {chat_id}.")

    except Exception as e:
        logger.critical(f"🔥 [WatchdogJob] Failed to start scheduler: {e}")
