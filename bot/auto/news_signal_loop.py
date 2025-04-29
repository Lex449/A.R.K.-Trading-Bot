"""
A.R.K. News Signal Loop – Ultra Premium Real-Time News Trader.
Monitors latest stock news and sends instant trading alerts if relevant events occur.
"""

import asyncio
from telegram import Bot
from bot.engine.news_scanner import detect_breaking_news, format_breaking_news
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings
from bot.utils.error_reporter import report_error

# Setup logger and load config
logger = setup_logger(__name__)
config = get_settings()

bot_token = config["TELEGRAM_TOKEN"]
chat_id = int(config["TELEGRAM_CHAT_ID"])
language = config.get("BOT_LANGUAGE", "en")

async def news_signal_loop():
    """
    Permanent loop to scan for breaking news and send premium alerts.
    """
    bot = Bot(token=bot_token)

    logger.info("📰 [NewsLoop] Starting real-time news monitoring...")

    while True:
        try:
            breaking_news = await detect_breaking_news()

            if breaking_news:
                message = await format_breaking_news(breaking_news, lang=language)

                if message:
                    await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown", disable_web_page_preview=True)
                    logger.info(f"✅ [NewsLoop] Breaking news alert sent. Articles: {len(breaking_news)}")

            await asyncio.sleep(300)  # 5 Minuten Pause

        except Exception as e:
            logger.error(f"❌ [NewsLoop] Fatal error: {e}")
            await report_error(bot, chat_id, e, context_info="News Signal Loop Crash")
            await asyncio.sleep(60)  # Kleine Pause bei Fehler
