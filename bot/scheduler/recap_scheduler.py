"""
A.R.K. Recap Scheduler – Daily & Weekly Trade Performance Recap.
Automatisch. Menschlich. Motivierend. NASA Style.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Bot
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.analytics.performance_tracker import generate_daily_recap, generate_weekly_recap
from bot.config.settings import get_settings

# Logger & Config
logger = setup_logger(__name__)
config = get_settings()

# Recap Scheduler Global
recap_scheduler = AsyncIOScheduler()

async def send_recap(bot: Bot, chat_id: int, mode: str = "daily"):
    """
    Sends a recap message (daily or weekly).
    """
    try:
        if mode == "daily":
            recap = generate_daily_recap()
            title = "📈 *Daily Performance Recap*"
        elif mode == "weekly":
            recap = generate_weekly_recap()
            title = "📊 *Weekly Summary Report*"
        else:
            logger.warning(f"[Recap] Invalid mode: {mode}")
            return

        if recap:
            message = f"{title}\n\n{recap}"
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            logger.info(f"✅ [Recap] {mode.capitalize()} recap sent.")
        else:
            logger.info(f"ℹ️ [Recap] No {mode} recap data to send.")

    except Exception as e:
        logger.error(f"❌ [Recap] {mode} recap error: {e}")
        await report_error(bot, chat_id, e, context_info=f"{mode.capitalize()} Recap")

def start_recap_scheduler(bot: Bot, chat_id: int):
    """
    Starts both daily and weekly recap jobs.
    """
    try:
        recap_scheduler.remove_all_jobs()

        # Daily Recap – every trading day at 22:30 CET (16:30 ET)
        recap_scheduler.add_job(
            send_recap,
            trigger=CronTrigger(hour=22, minute=30, timezone="Europe/Berlin"),
            args=[bot, chat_id, "daily"],
            id="daily_recap_job",
            name="Daily Performance Recap"
        )

        # Weekly Recap – every Friday at 22:35 CET
        recap_scheduler.add_job(
            send_recap,
            trigger=CronTrigger(day_of_week="fri", hour=22, minute=35, timezone="Europe/Berlin"),
            args=[bot, chat_id, "weekly"],
            id="weekly_recap_job",
            name="Weekly Summary Recap"
        )

        if not recap_scheduler.running:
            recap_scheduler.start()

        logger.info("✅ [RecapScheduler] Daily & Weekly Recap Jobs started.")

    except Exception as e:
        logger.critical(f"🔥 [RecapScheduler] Startup failed: {e}")
