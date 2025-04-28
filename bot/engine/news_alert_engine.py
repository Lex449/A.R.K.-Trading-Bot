"""
A.R.K. News Alert Engine – Ultra Premium Breaking News Detection.
Finnhub First, Yahoo Finance Backup. Optimized for Speed, Relevance, and Multilingual Alerts.
"""

import aiohttp
from datetime import datetime
from bot.config.settings import get_settings
from bot.utils.news_health_checker import use_finnhub
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()
finnhub_api_key = config.get("FINNHUB_API_KEY")
symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

# API Endpoints
FINNHUB_ENDPOINT = f"https://finnhub.io/api/v1/news?category=general&token={finnhub_api_key}"
YAHOO_ENDPOINT_TEMPLATE = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"

# Critical keywords triggering alerts
IMPORTANT_KEYWORDS = [
    "inflation", "rate hike", "recession", "crash", "bankruptcy",
    "fed", "layoffs", "defaults", "market turmoil", "collapse",
    "interest rates", "geopolitical", "fomc", "earnings warning"
]

async def fetch_finnhub_news() -> list:
    """Fetches the latest general market news from Finnhub."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FINNHUB_ENDPOINT, timeout=10) as response:
                if response.status == 200:
                    news = await response.json()
                    logger.info("[News Engine] Finnhub news fetched successfully.")
                    return news
    except Exception as e:
        logger.warning(f"[News Engine] Error fetching Finnhub news: {e}")
    return []

async def fetch_yahoo_news(symbol: str) -> str:
    """Fetches RSS feed headlines from Yahoo Finance."""
    try:
        async with aiohttp.ClientSession() as session:
            url = YAHOO_ENDPOINT_TEMPLATE.format(symbol=symbol)
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    rss = await response.text()
                    logger.info(f"[News Engine] Yahoo news fetched for {symbol}.")
                    return rss
    except Exception as e:
        logger.warning(f"[News Engine] Error fetching Yahoo news for {symbol}: {e}")
    return ""

async def detect_breaking_news() -> list:
    """Detects important breaking news headlines."""
    breaking_news = []
    now = datetime.utcnow()

    if use_finnhub():
        news_list = await fetch_finnhub_news()
        for article in news_list:
            try:
                published_time = datetime.utcfromtimestamp(article.get("datetime", 0))
                age_minutes = (now - published_time).total_seconds() / 60
                if age_minutes > 20:
                    continue

                headline = article.get("headline", "").lower()
                if any(keyword in headline for keyword in IMPORTANT_KEYWORDS):
                    breaking_news.append({
                        "headline": article.get("headline", ""),
                        "source": article.get("source", "Unknown"),
                        "url": article.get("url", "")
                    })
            except Exception:
                continue
    else:
        for symbol in symbols:
            raw_rss = await fetch_yahoo_news(symbol)
            if any(keyword in raw_rss.lower() for keyword in IMPORTANT_KEYWORDS):
                breaking_news.append({
                    "headline": f"Important event detected for {symbol}",
                    "source": "Yahoo Finance RSS",
                    "url": f"https://finance.yahoo.com/quote/{symbol}"
                })

    return breaking_news

async def format_breaking_news(news_list: list, lang: str = "en") -> str:
    """Formats the breaking news headlines into a single message."""
    if not news_list:
        return ""

    if lang == "de":
        header = "📰 *Breaking News erkannt!*"
        footer = "\n_Aktuelle Ereignisse könnten den Markt stark beeinflussen._"
    else:
        header = "📰 *Breaking News Detected!*"
        footer = "\n_Current events may heavily impact the market._"

    parts = [header]

    for news in news_list:
        headline = news.get("headline", "No headline available")
        source = news.get("source", "Unknown")
        url = news.get("url", "#")

        parts.append(f"• *{headline}*\nSource: `{source}`\n[Details]({url})")

    parts.append(footer)

    return "\n\n".join(parts)
