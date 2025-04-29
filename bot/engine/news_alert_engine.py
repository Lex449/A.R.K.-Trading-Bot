"""
A.R.K. Breaking News Engine Ultra 2.0 – Hyper-Intelligent Detection System.
Detects real breaking news events with Power-Scored Adaptive Keyword Intelligence.

Built for: Institutional-Grade News Trading & Real-Time Market Domination.
"""

import aiohttp
from datetime import datetime
from bot.config.settings import get_settings
from bot.utils.news_health_checker import use_finnhub
from bot.utils.keyword_enricher import get_all_keywords, get_keyword_power
from bot.utils.logger import setup_logger

# === Setup ===
logger = setup_logger(__name__)
config = get_settings()

# === API Endpoints ===
FINNHUB_API_KEY = config.get("FINNHUB_API_KEY")
FINNHUB_ENDPOINT = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"
YAHOO_ENDPOINT_TEMPLATE = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

# === Breaking News Settings ===
BASE_THRESHOLD = 6
POWER_THRESHOLD = 8

# === Core News Fetchers ===
async def fetch_finnhub_news() -> list:
    """Fetches latest news headlines from Finnhub."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FINNHUB_ENDPOINT, timeout=10) as response:
                if response.status == 200:
                    news = await response.json()
                    logger.info("[News Engine] ✅ Finnhub news fetched.")
                    return news
    except Exception as e:
        logger.warning(f"[News Engine] ⚠️ Finnhub fetch error: {e}")
    return []

async def fetch_yahoo_news(symbol: str) -> str:
    """Fetches RSS feed for a specific symbol from Yahoo Finance."""
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

# === Breaking News Detection Core ===
async def detect_breaking_news() -> list:
    """
    Detects critical breaking news events using Power Scoring Intelligence.
    Prioritizes Finnhub, Yahoo as backup.
    Returns: List of highly relevant headlines.
    """
    breaking_news = []
    now = datetime.utcnow()
    keywords = get_all_keywords()
    keyword_power = get_keyword_power()

    try:
        if use_finnhub():
            news_items = await fetch_finnhub_news()
            for article in news_items:
                published_time = datetime.utcfromtimestamp(article.get("datetime", 0))
                age_minutes = (now - published_time).total_seconds() / 60
                headline = article.get("headline", "")

                if age_minutes <= 20 and _is_breaking_headline(headline, keywords, keyword_power):
                    breaking_news.append({
                        "headline": article.get("headline", "No headline"),
                        "source": article.get("source", "Unknown"),
                        "url": article.get("url", "#")
                    })
        else:
            for symbol in symbols:
                raw_rss = await fetch_yahoo_news(symbol)
                if any(_is_breaking_headline(line, keywords, keyword_power) for line in raw_rss.lower().splitlines()):
                    breaking_news.append({
                        "headline": f"Significant Event for {symbol}",
                        "source": "Yahoo Finance RSS",
                        "url": f"https://finance.yahoo.com/quote/{symbol}"
                    })

    except Exception as e:
        logger.error(f"❌ [News Engine] Critical news detection failure: {e}")

    return breaking_news

# === Headline Evaluation Engine ===
def _is_breaking_headline(headline: str, keywords: list, power_map: dict) -> bool:
    """
    Determines if a headline is critical enough to trigger an alert.
    Applies Power-Based Dynamic Thresholds.
    """
    score = 0
    headline_lower = headline.lower()

    for keyword in keywords:
        if keyword in headline_lower:
            base_weight = 4
            power_bonus = power_map.get(keyword, 0) * 0.5
            score += base_weight + power_bonus

    logger.debug(f"[News Scoring] Headline: {headline} | Score: {score:.2f}")

    return score >= POWER_THRESHOLD

# === Formatter for Telegram Message ===
async def format_breaking_news(news_list: list, lang: str = "en") -> str:
    """Formats detected breaking news into a structured Telegram message."""
    if not news_list:
        return ""

    header = "📰 *Breaking News Detected!*" if lang == "en" else "📰 *Breaking News erkannt!*"
    footer = "_Markets react fast. Stay sharp._" if lang == "en" else "_Märkte reagieren blitzschnell. Bleib wachsam._"

    parts = [header]

    for news in news_list:
        headline = news.get("headline", "No headline available")
        source = news.get("source", "Unknown")
        url = news.get("url", "#")
        parts.append(f"• *{headline}*\n_Source: {source}_\n[More Details]({url})")

    parts.append(footer)

    return "\n\n".join(parts)
