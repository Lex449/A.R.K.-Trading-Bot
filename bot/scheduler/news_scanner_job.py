"""
A.R.K. News Scanner Job – Smart US Session Breakout Monitor.
Scans for breaking market news only during trading hours or 30 min before.
Built for: Efficiency, API Protection, Ultra Premium Alerts.
"""

import asyncio
from telegram import Bot
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.engine.news_alert_engine import detect_breaking_news, format_breaking_news
from bot.utils.market_session_guard import is_us_market_open, minutes_until_market_open
from bot.utils.api_bridge import record_call  # ✅ Korrekte neue Quelle

# === Setup ===
logger = setup_logger(__name__)
config = get_settings()

bot_token = config["BOT_TOKEN"]
chat_id = int(config["TELEGRAM_CHAT_ID"])
language = config.get("BOT_LANGUAGE", "en")

async def news_scanner_job():
    """
    Permanent loop that only scans when market is open or 30 minutes before.
    """
    bot = Bot(token=bot_token)

    logger.info("🛰️ [NewsScanner] Initialized – waiting for market hours...")

    while True:
        try:
            # === Market-Time Check ===
            market_open = is_us_market_open()
            pre_market = minutes_until_market_open() <= 30

            if market_open or pre_market:
                logger.info("📰 [NewsScanner] Running news scan...")
                record_call("finnhub")  # Falls dein Monitor aktiv ist

                breaking_news = await detect_breaking_news()
                if breaking_news:
                    message = await format_breaking_news(breaking_news, lang=language)
                    if message:
                        await bot.send_message(
                            chat_id=chat_id,
                            text=message,
                            parse_mode="Markdown",
                            disable_web_page_preview=True
                        )
                        logger.info(f"✅ [NewsScanner] Sent alert – {len(breaking_news)} articles.")
                else:
                    logger.info("ℹ️ [NewsScanner] No relevant news found.")

                await asyncio.sleep(300)  # 5 min cool-down
            else:
                logger.info("⏳ [NewsScanner] Market closed. Sleeping 10 min.")
                await asyncio.sleep(600)

        except Exception as e:
            logger.error(f"❌ [NewsScanner] Critical failure: {e}")
            await report_error(bot, chat_id, e, context_info="News Scanner Loop")
            await asyncio.sleep(60)

# === Exported wrapper for startup ===
def start_news_scanner_job(application):
    asyncio.create_task(news_scanner_job())
