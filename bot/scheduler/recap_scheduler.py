"""
A.R.K. Recap Scheduler – Daily & Weekly Ultra Performance Reports
Fully automated, multilingual, timezone-friendly.
Made in Bali. Engineered with German Precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram import Bot
from bot.analytics.performance_tracker import get_performance_summary
from bot.analytics.win_loss_report import generate_win_loss_report
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings

# === Logger & Config ===
logger = setup_logger(__name__)
config = get_settings()

# Telegram Setup
bot_token = config["BOT_TOKEN"]
chat_id = int(config["TELEGRAM_CHAT_ID"])
language = config.get("BOT_LANGUAGE", "en")

# === Scheduler Global ===
recap_scheduler = AsyncIOScheduler()

async def send_recap(bot: Bot, chat_id: int, mode: str = "daily"):
    """
    Sends a recap message (daily or weekly) dynamically.
    """

    try:
        if mode == "daily":
            report_text = get_performance_summary(lang=language)
            title = get_text("daily_recap", language)
        elif mode == "weekly":
            report_text = generate_win_loss_report(lang=language)
            title = get_text("weekly_recap", language)
        else:
            logger.warning(f"[RecapScheduler] Invalid mode: {mode}")
            return

        if report_text:
            message = f"📈 *{title}*\n\n{report_text}"
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown", disable_web_page_preview=True)
            logger.info(f"✅ [RecapScheduler] {mode.capitalize()} recap sent successfully.")
        else:
            logger.info(f"ℹ️ [RecapScheduler] No {mode} recap available today.")

    except Exception as e:
        logger.error(f"❌ [RecapScheduler] Failed to send {mode} recap: {e}")
        await report_error(bot, chat_id, e, context_info=f"{mode.capitalize()} Recap Error")

def start_recap_scheduler(bot: Bot, chat_id: int):
    """
    Initializes the daily and weekly recap jobs with timezone flexibility.
    """

    try:
        recap_scheduler.remove_all_jobs()

        # === Daily Recap (e.g. CET 22:30) ===
        recap_scheduler.add_job(
            send_recap,
            trigger=CronTrigger(hour=22, minute=30, timezone="Europe/Berlin"),
            args=[bot, chat_id, "daily"],
            id="daily_recap_job",
            name="Daily Recap",
            replace_existing=True
        )

        # === Weekly Recap (e.g. CET Friday 22:35) ===
        recap_scheduler.add_job(
            send_recap,
            trigger=CronTrigger(day_of_week="fri", hour=22, minute=35, timezone="Europe/Berlin"),
            args=[bot, chat_id, "weekly"],
            id="weekly_recap_job",
            name="Weekly Recap",
            replace_existing=True
        )

        if not recap_scheduler.running:
            recap_scheduler.start()

        logger.info("✅ [RecapScheduler] Daily & Weekly Recap Scheduler started successfully.")

    except Exception as e:
        logger.critical(f"🔥 [RecapScheduler] Critical startup failure: {e}")
