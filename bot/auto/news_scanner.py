# bot/engine/news_scanner.py

"""
A.R.K. News Scanner Engine – High Precision Market Alerts.
Scans for breaking financial news and formats multilingual output.
Powered by Finnhub and custom filters.
"""

import logging
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.utils.error_reporter import report_error
import httpx

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

FINNHUB_API_KEY = config.get("FINNHUB_API_KEY")
NEWS_FILTER_ENABLED = config.get("NEWS_FILTER_ENABLED", True)
BACKUP_NEWS_ENABLED = config.get("BACKUP_NEWS_ENABLED", True)

async def detect_breaking_news() -> list:
    """
    Scans for breaking news using the Finnhub API.
    Returns:
        list: Filtered list of important news articles.
    """
    try:
        if not NEWS_FILTER_ENABLED:
            logger.info("📰 [NewsScanner] News filter disabled.")
            return []

        url = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"

        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch news. Status code: {response.status_code}")

        articles = response.json()

        # Filter only high-impact articles
        breaking_news = [
            article for article in articles
            if "interest rate" in article["headline"].lower()
            or "fed" in article["headline"].lower()
            or "inflation" in article["headline"].lower()
            or "recession" in article["headline"].lower()
        ]

        logger.info(f"🧠 [NewsScanner] {len(breaking_news)} breaking news detected.")
        return breaking_news

    except Exception as e:
        logger.error(f"❌ [NewsScanner] Error detecting news: {e}")
        return []

async def format_breaking_news(news_list: list, lang: str = "en") -> str:
    """
    Formats breaking news list into a Telegram-ready string.
    Args:
        news_list (list): List of news dicts.
        lang (str): Language for output.
    Returns:
        str: Markdown-formatted news summary.
    """
    try:
        if not news_list:
            return ""

        formatted = f"🗞️ *{get_text('signal_ultra_premium', lang)}*\n\n"

        for news in news_list[:3]:  # Only top 3 news
            headline = news.get("headline", "")
            source = news.get("source", "")
            url = news.get("url", "")
            formatted += f"*{headline}*  \n`{source}` → [Link]({url})\n\n"

        formatted += get_text("signal_footer", lang)

        return formatted

    except Exception as e:
        logger.error(f"❌ [NewsFormatter] Error formatting news: {e}")
        return "⚠️ Error generating news output."
