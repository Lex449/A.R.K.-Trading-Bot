"""
A.R.K. News Scanner Job – Smart US Session Breakout Monitor v2025.7
Scans for breaking news during US trading hours or 30 min prior.
Built for: API Protection, Efficiency, Real-Time Signal Detection.
Made in Bali. Engineered with German Precision.
"""

import asyncio
from telegram.ext import Application
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.language import get_language
from bot.utils.error_reporter import report_error
from bot.engine.news_alert_engine import detect_breaking_news, format_breaking_news
from bot.utils.market_session_guard import is_us_market_open, minutes_until_market_open
from bot.utils.api_bridge import record_call

logger = setup_logger(__name__)
config = get_settings()

is_scanner_running = False  # Block multiple parallel starts

async def news_scanner_job(application: Application):
    global is_scanner_running
    if is_scanner_running:
        logger.warning("⚠️ [NewsScanner] Already running. Skipping duplicate launch.")
        return
    is_scanner_running = True

    bot = application.bot
    chat_id = int(config["TELEGRAM_CHAT_ID"])
    lang = get_language(chat_id) or config.get("BOT_LANGUAGE", "en")

    logger.info("🛰️ [NewsScanner] Initialized. Awaiting market hours...")

    while True:
        try:
            market_open = is_us_market_open()
            pre_market = minutes_until_market_open() <= 30

            if market_open or pre_market:
                logger.info("📰 [NewsScanner] Running market news scan...")
                record_call("finnhub")

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
                        logger.info(f"✅ [NewsScanner] Alert sent – {len(breaking_news)} article(s).")
                else:
                    logger.info("ℹ️ [NewsScanner] No relevant news found.")

                await asyncio.sleep(300)  # Cooldown: 5 Minuten
            else:
                logger.info("⏳ [NewsScanner] Market closed – sleep 10 min.")
                await asyncio.sleep(600)

        except Exception as e:
            logger.error(f"❌ [NewsScanner] Fatal error: {e}")
            await report_error(bot, chat_id, e, context_info="News Scanner Loop")
            await asyncio.sleep(90)  # Stabilitätswartezeit bei Fehlern

def start_news_scanner_job(application: Application):
    asyncio.create_task(news_scanner_job(application))
