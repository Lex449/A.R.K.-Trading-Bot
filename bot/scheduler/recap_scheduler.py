"""
A.R.K. Recap Scheduler – Daily & Weekly Ultra Performance Reports
Handles multilingual summary generation with auto-recovery.
Made in Bali. Engineered with German Precision.
"""

from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.config.settings import get_settings
from bot.utils.session_tracker import get_session_data
from bot.analytics.win_loss_report import generate_win_loss_report
from bot.utils.error_reporter import report_error

# Setup
logger = setup_logger(__name__)
config = get_settings()
scheduler = AsyncIOScheduler()

def get_performance_summary(lang: str = "en") -> str:
    """
    Generates a multilingual summary of today's signal performance.
    """

    try:
        data = get_session_data()
        if not data:
            return get_text("no_data_today", lang)

        total = data.get("signals_total", 0)
        strong = data.get("strong_signals", 0)
        moderate = data.get("moderate_signals", 0)
        weak = data.get("weak_signals", 0)
        stars = round(data.get("total_confidence", 0.0), 2)

        summary = (
            f"{get_text('signals_total', lang)}: *{total}*\n"
            f"{get_text('strong_signals', lang)}: *{strong}*\n"
            f"{get_text('moderate_signals', lang)}: *{moderate}*\n"
            f"{get_text('weak_signals', lang)}: *{weak}*\n"
            f"{get_text('avg_confidence', lang)}: *{stars} ⭐️*"
        )

        return summary

    except Exception as e:
        logger.error(f"[Recap] Summary generation failed: {e}")
        return f"⚠️ {get_text('summary_failed', lang)}\nError: {e}"

async def send_recap(bot: Bot, chat_id: int, mode: str = "daily"):
    """
    Sends a daily or weekly recap message with multilingual formatting.
    """

    try:
        language = config.get("BOT_LANGUAGE", "en")

        if mode == "daily":
            text = get_performance_summary(lang=language)
            title = get_text("daily_recap", language)
        elif mode == "weekly":
            text = generate_win_loss_report(lang=language)
            title = get_text("weekly_recap", language)
        else:
            logger.warning(f"[RecapScheduler] Unknown mode: {mode}")
            return

        message = f"📈 *{title}*\n\n{text}"
        await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown", disable_web_page_preview=True)

        logger.info(f"✅ [RecapScheduler] {mode.capitalize()} recap sent successfully.")

    except Exception as e:
        logger.error(f"❌ [RecapScheduler] Failed to send {mode} recap: {e}")
        await report_error(bot, chat_id, e, context_info=f"{mode.capitalize()} Recap Error")

def start_recap_scheduler(bot: Bot, chat_id: int):
    """
    Starts the automated recap jobs (daily and weekly) based on configured timezones.
    """

    try:
        scheduler.remove_all_jobs()

        # === Daily Recap ===
        scheduler.add_job(
            send_recap,
            trigger=CronTrigger(hour=22, minute=30, timezone="Europe/Berlin"),
            args=[bot, chat_id, "daily"],
            id="daily_recap_job",
            name="Daily Recap",
            replace_existing=True
        )

        # === Weekly Recap ===
        scheduler.add_job(
            send_recap,
            trigger=CronTrigger(day_of_week="fri", hour=22, minute=35, timezone="Europe/Berlin"),
            args=[bot, chat_id, "weekly"],
            id="weekly_recap_job",
            name="Weekly Recap",
            replace_existing=True
        )

        if not scheduler.running:
            scheduler.start()

        logger.info("✅ [RecapScheduler] Scheduler started successfully.")

    except Exception as e:
        logger.critical(f"🔥 [RecapScheduler] Startup error: {e}")
