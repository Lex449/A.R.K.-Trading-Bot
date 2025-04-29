"""
A.R.K. News Scheduler – Breaking News Scanner 2025.
Wacht über relevante Marktnews für alle Symbole aus deiner .env.
"""

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from telegram import Bot
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings
from bot.utils.error_reporter import report_error
from bot.engine.news_alert_engine import detect_breaking_news, format_breaking_news  # <<< KORRIGIERT

# Logger & Config
logger = setup_logger(__name__)
config = get_settings()

# News Scheduler Global
news_scheduler = AsyncIOScheduler()

async def news_scan_task(bot: Bot, chat_id: int, symbols: list[str], lang: str = "en"):
    """
    Performs a news scan for all configured symbols.
    Sends alerts for breaking news.
    """
    try:
        logger.info("📰 [NewsJob] Scanning for breaking news...")

        breaking_news = await detect_breaking_news()

        if breaking_news:
            message = await format_breaking_news(breaking_news, lang=lang)

            if message:
                await bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode="Markdown",
                    disable_web_page_preview=True
                )
                logger.info(f"✅ [NewsJob] Alert sent – {len(breaking_news)} news items detected.")
        else:
            logger.info("ℹ️ [NewsJob] No relevant news found.")

    except Exception as e:
        logger.error(f"❌ [NewsJob] Fatal Error: {e}")
        await report_error(bot, chat_id, e, context_info="News Scheduler")

def start_news_scheduler(bot: Bot, chat_id: int):
    """
    Starts the news scan job for all configured symbols every 5 minutes.
    """
    try:
        # Prepare symbols and language
        symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])
        language = config.get("BOT_LANGUAGE", "en")

        # Kill existing jobs if any
        news_scheduler.remove_all_jobs()

        news_scheduler.add_job(
            news_scan_task,
            trigger=IntervalTrigger(minutes=5),
            args=[bot, chat_id, symbols, language],
            id=f"breaking_news_scanner_{chat_id}",
            replace_existing=True,
            name=f"A.R.K. News Scanner for {chat_id}",
            misfire_grace_time=120
        )

        if not news_scheduler.running:
            news_scheduler.start()

        logger.info(f"✅ [NewsScheduler] Started for chat {chat_id}, scanning {len(symbols)} symbols.")

    except Exception as e:
        logger.critical(f"🔥 [NewsScheduler] Could not start: {e}")
