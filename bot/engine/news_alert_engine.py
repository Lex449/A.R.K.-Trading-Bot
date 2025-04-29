"""
A.R.K. News Alert Engine – Ultra Money Machine 5.0
Dual-Source News Scanner: Finnhub + Yahoo Backup.
Live Breaking Detection | Multilingual Alerts | Market Impact Warnings.

Engineered for: Lightning Speed, Zero Failure Rates, Institutional-Grade Risk Management.
"""

import aiohttp
from datetime import datetime
from bot.config.settings import get_settings
from bot.utils.news_health_checker import use_finnhub
from bot.utils.breaking_news_filter import is_breaking_news
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

# API Access
finnhub_api_key = config.get("FINNHUB_API_KEY")
symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

FINNHUB_ENDPOINT = f"https://finnhub.io/api/v1/news?category=general&token={finnhub_api_key}"
YAHOO_ENDPOINT_TEMPLATE = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"

async def fetch_finnhub_news() -> list:
    """Fetches latest general news headlines from Finnhub API."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FINNHUB_ENDPOINT, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info("✅ [NewsEngine] Finnhub news fetched.")
                    return data
    except Exception as e:
        logger.warning(f"⚠️ [NewsEngine] Finnhub error: {e}")
    return []

async def fetch_yahoo_news(symbol: str) -> str:
    """Fetches latest news headlines via Yahoo Finance RSS."""
    try:
        async with aiohttp.ClientSession() as session:
            url = YAHOO_ENDPOINT_TEMPLATE.format(symbol=symbol)
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    rss_content = await response.text()
                    logger.info(f"✅ [NewsEngine] Yahoo RSS fetched for {symbol}.")
                    return rss_content
    except Exception as e:
        logger.warning(f"⚠️ [NewsEngine] Yahoo fetch error: {e}")
    return ""

async def detect_breaking_news() -> list:
    """
    Detects real-time critical news affecting the markets.
    Primary: Finnhub | Fallback: Yahoo RSS.
    Returns list of high-impact news articles.
    """
    breaking_news = []
    now = datetime.utcnow()

    if use_finnhub():
        news_feed = await fetch_finnhub_news()
        for article in news_feed:
            try:
                headline = article.get("headline", "")
                timestamp = datetime.utcfromtimestamp(article.get("datetime", 0))
                age_minutes = (now - timestamp).total_seconds() / 60

                if headline and age_minutes <= 20 and is_breaking_news(headline):
                    breaking_news.append({
                        "headline": headline,
                        "source": article.get("source", "Unknown"),
                        "url": article.get("url", "#")
                    })
            except Exception as e:
                logger.warning(f"⚠️ [NewsEngine] Minor Finnhub parsing error: {e}")
    else:
        for symbol in symbols:
            raw_rss = await fetch_yahoo_news(symbol)
            if any(is_breaking_news(line) for line in raw_rss.lower().splitlines()):
                breaking_news.append({
                    "headline": f"Breaking Event for {symbol}",
                    "source": "Yahoo Finance RSS",
                    "url": f"https://finance.yahoo.com/quote/{symbol}"
                })

    return breaking_news

async def format_breaking_news(news_list: list, lang: str = "en") -> str:
    """Formats the breaking news list into a clean Telegram message."""
    if not news_list:
        return ""

    header = "📰 *Breaking News Detected!*" if lang.lower() == "en" else "📰 *Breaking News erkannt!*"
    footer = "_News can heavily impact market momentum._" if lang.lower() == "en" else "_Nachrichten können Marktbewegungen stark beeinflussen._"

    message_parts = [header]

    for news in news_list:
        headline = news.get("headline", "No headline available")
        source = news.get("source", "Unknown")
        url = news.get("url", "#")
        message_parts.append(f"• *{headline}*\n_Source: {source}_\n[More Details]({url})")

    message_parts.append(footer)

    return "\n\n".join(message_parts)
