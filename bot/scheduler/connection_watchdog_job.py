"""
A.R.K. Scheduler – Connection Watchdog Monitor 2025.6
Permanently monitors Telegram API connectivity. Sends multilingual alerts on disruption.
Made in Bali. Engineered with German Precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram import Bot
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings

logger = setup_logger(__name__)
config = get_settings()
watchdog_scheduler = AsyncIOScheduler()

async def check_connection(bot: Bot, chat_id: int):
    """
    Verifies Telegram Bot API connection health.
    """
    lang = get_language(chat_id) or "en"
    try:
        await bot.get_me()
        logger.info("✅ [Watchdog] Telegram connection OK.")

    except Exception as e:
        logger.error(f"❌ [Watchdog] Connection failure: {e}")

        try:
            text = get_text("connection_lost", lang)
            await bot.send_message(
                chat_id=chat_id,
                text=f"⚠️ *{text}*",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
            logger.info("⚠️ [Watchdog] Alert message sent to admin.")

        except Exception as alert_error:
            logger.critical(f"🔥 [Watchdog] Failed to send alert: {alert_error}")

        await report_error(bot, chat_id, e, context_info="Watchdog Failure")

def start_connection_watchdog(bot: Bot, chat_id: int):
    """
    Starts the watchdog job, runs every 30 minutes.
    """
    try:
        job_id = f"connection_watchdog_job_{chat_id}"

        if watchdog_scheduler.get_job(job_id):
            logger.info(f"♻️ [Watchdog] Already running for {chat_id}")
            return

        watchdog_scheduler.add_job(
            check_connection,
            trigger=IntervalTrigger(minutes=30),
            args=[bot, chat_id],
            id=job_id,
            replace_existing=True,
            name=f"A.R.K. Connection Watchdog for Chat {chat_id}",
            misfire_grace_time=300
        )

        if not watchdog_scheduler.running:
            watchdog_scheduler.start()

        logger.info(f"✅ [Watchdog] Scheduler started for chat_id {chat_id}")

    except Exception as e:
        logger.critical(f"🔥 [Watchdog] Scheduler init error: {e}")
