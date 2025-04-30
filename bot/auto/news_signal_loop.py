"""
A.R.K. News Signal Loop – Ultra Premium Real-Time News Trader.
Monitors latest stock news and sends instant trading alerts if relevant events occur.
"""

import asyncio
from telegram import Bot
from bot.engine.news_scanner import detect_breaking_news, format_breaking_news
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings
from bot.utils.market_session_guard import is_us_market_open
from bot.utils.error_reporter import report_error

# Setup logger and load config
logger = setup_logger(__name__)
config = get_settings()

bot_token = config["TELEGRAM_TOKEN"]
chat_id = int(config["TELEGRAM_CHAT_ID"])
language = config.get("BOT_LANGUAGE", "en")

async def news_signal_loop():
    """
    Permanent loop to scan for breaking news and send premium alerts
    only during US market sessions.
    """
    bot = Bot(token=bot_token)
    logger.info("📰 [NewsLoop] Initialized – News scanner activated.")

    while True:
        try:
            # === US Market Guard ===
            if not is_us_market_open():
                logger.info("⏳ [NewsLoop] US market closed – skipping news check.")
                await asyncio.sleep(180)
                continue

            # === Fetch & Format ===
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
                    logger.info(f"✅ [NewsLoop] Breaking news alert sent. Count: {len(breaking_news)}")
                else:
                    logger.info("ℹ️ [NewsLoop] No formatable news message.")

            else:
                logger.info("🔎 [NewsLoop] No relevant news found this cycle.")

            await asyncio.sleep(300)  # 5 min sleep

        except Exception as e:
            logger.error(f"❌ [NewsLoop] Fatal error occurred: {e}")
            await report_error(bot, chat_id, e, context_info="News Signal Loop Crash")
            await asyncio.sleep(60)  # Wait before retry
