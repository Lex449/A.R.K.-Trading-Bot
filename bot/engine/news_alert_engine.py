"""
A.R.K. News Alert Engine – Ultra Premium 3.0
Dual-Source Breaking News Detection System:
Primary: Finnhub | Backup: Yahoo Finance RSS
Built for Ultra-Fast Impact Scanning, Multilingual Alerting & Future AI Expansion.
"""

import aiohttp
from datetime import datetime
from bot.config.settings import get_settings
from bot.utils.news_health_checker import use_finnhub
from bot.utils.breaking_news_filter import is_breaking_news
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

# Load Config
config = get_settings()
finnhub_api_key = config.get("FINNHUB_API_KEY")
symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

# API Endpoints
FINNHUB_ENDPOINT = f"https://finnhub.io/api/v1/news?category=general&token={finnhub_api_key}"
YAHOO_ENDPOINT_TEMPLATE = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"

async def fetch_finnhub_news() -> list:
    """Fetches latest general news headlines from Finnhub."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FINNHUB_ENDPOINT, timeout=10) as response:
                if response.status == 200:
                    news = await response.json()
                    logger.info("[News Engine] ✅ Finnhub news fetched successfully.")
                    return news
    except Exception as e:
        logger.warning(f"[News Engine] ⚠️ Finnhub fetch error: {e}")
    return []

async def fetch_yahoo_news(symbol: str) -> str:
    """Fetches RSS news for a specific symbol from Yahoo Finance."""
    try:
        async with aiohttp.ClientSession() as session:
            url = YAHOO_ENDPOINT_TEMPLATE.format(symbol=symbol)
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    rss = await response.text()
                    logger.info(f"[News Engine] ✅ Yahoo RSS fetched for {symbol}.")
                    return rss
    except Exception as e:
        logger.warning(f"[News Engine] ⚠️ Yahoo RSS fetch error for {symbol}: {e}")
    return ""

async def detect_breaking_news() -> list:
    """
    Detects critical breaking news events.
    Prioritizes Finnhub, uses Yahoo RSS as fallback.
    Returns list of relevant headlines.
    """
    breaking_news = []
    now = datetime.utcnow()

    if use_finnhub():
        news_items = await fetch_finnhub_news()
        for article in news_items:
            try:
                published_time = datetime.utcfromtimestamp(article.get("datetime", 0))
                age_minutes = (now - published_time).total_seconds() / 60
                headline = article.get("headline", "")

                if age_minutes <= 20 and is_breaking_news(headline):
                    breaking_news.append({
                        "headline": article.get("headline", "No headline"),
                        "source": article.get("source", "Unknown"),
                        "url": article.get("url", "#")
                    })
            except Exception as e:
                logger.warning(f"[News Engine] Minor parsing error: {e}")
    else:
        for symbol in symbols:
            raw_rss = await fetch_yahoo_news(symbol)
            if any(is_breaking_news(line) for line in raw_rss.lower().splitlines()):
                breaking_news.append({
                    "headline": f"Significant Event for {symbol}",
                    "source": "Yahoo Finance RSS",
                    "url": f"https://finance.yahoo.com/quote/{symbol}"
                })

    return breaking_news

async def format_breaking_news(news_list: list, lang: str = "en") -> str:
    """Formats detected breaking news into a clean Telegram message."""
    if not news_list:
        return ""

    # Language Specific Texts
    header = "📰 *Breaking News Detected!*" if lang.lower() == "en" else "📰 *Breaking News erkannt!*"
    footer = "_Current events may impact the markets._" if lang.lower() == "en" else "_Aktuelle Ereignisse könnten die Märkte beeinflussen._"

    parts = [header]

    for news in news_list:
        headline = news.get("headline", "No headline available")
        source = news.get("source", "Unknown")
        url = news.get("url", "#")
        parts.append(f"• *{headline}*\n_Source: {source}_\n[More Details]({url})")

    parts.append(footer)

    return "\n\n".join(parts)
