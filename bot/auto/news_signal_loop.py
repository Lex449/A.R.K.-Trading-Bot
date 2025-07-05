"""
A.R.K. News Signal Loop – Ultra Premium Real-Time News Trader.
Monitors latest stock news and sends instant trading alerts if relevant events occur.
"""

import asyncio
from telegram import Bot
from bot.engine.news_scanner import detect_breaking_news, format_breaking_news
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings
from bot.utils.market_session_guard import is_us_market_session

logger = setup_logger(__name__)
settings = get_settings()

bot_token = settings["BOT_TOKEN"]
chat_id   = int(settings["TELEGRAM_CHAT_ID"])
language  = settings.get("BOT_LANGUAGE", "en")

async def news_signal_loop():
    """Infinite loop that polls breaking news and sends actionable alerts in real time."""
    bot = Bot(token=bot_token)
    logger.info("📡 [NewsLoop] Starting news polling loop...")

    while True:
        try:
            if is_us_market_session():
                news_items = await detect_breaking_news()
                if news_items:
                    text = format_breaking_news(news_items, language)
                    await bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")

            await asyncio.sleep(60)

        except Exception as e:
            logger.exception("⚠️ [NewsLoop] Error in news polling loop – continuing.")
            await asyncio.sleep(30)
