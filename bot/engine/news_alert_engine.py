# bot/engine/news_alert_engine.py

"""
A.R.K. Breaking News Engine – Ultra Reactive Intelligence 7.0
Real-Time Detection of Market-Moving Headlines with Adaptive Keyword Power Scoring.

Designed for: High-Frequency News Trading, Institutional Timing, Telegram Instant Alerts.
Made in Bali. Engineered with German Precision.
"""

import aiohttp
from datetime import datetime
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.keyword_enricher import get_all_keywords, get_keyword_power
from bot.utils.news_health_checker import use_finnhub

# === Setup ===
logger = setup_logger(__name__)
config = get_settings()
symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

# === API Sources ===
FINNHUB_KEY = config.get("FINNHUB_API_KEY")
FINNHUB_URL = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_KEY}"
YAHOO_RSS = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"

# === Scoring Settings ===
POWER_THRESHOLD = 8
MAX_AGE_MINUTES = 20

# === News Fetchers ===
async def fetch_finnhub_news() -> list:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FINNHUB_URL, timeout=10) as response:
                if response.status == 200:
                    news = await response.json()
                    logger.info("[News Engine] ✅ Finnhub news fetched.")
                    return news
    except Exception as e:
        logger.warning(f"[News Engine] ⚠️ Finnhub fetch error: {e}")
    return []

async def fetch_yahoo_news(symbol: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            url = YAHOO_RSS.format(symbol=symbol)
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    rss = await response.text()
                    logger.info(f"[News Engine] ✅ Yahoo RSS fetched for {symbol}")
                    return rss
    except Exception as e:
        logger.warning(f"[News Engine] ⚠️ Yahoo fetch error: {e}")
    return ""

# === Core News Detection ===
async def detect_breaking_news() -> list:
    breaking = []
    now = datetime.utcnow()
    keywords = get_all_keywords()
    power_map = get_keyword_power()

    try:
        if use_finnhub():
            items = await fetch_finnhub_news()
            for article in items:
                timestamp = datetime.utcfromtimestamp(article.get("datetime", 0))
                age_min = (now - timestamp).total_seconds() / 60
                headline = article.get("headline", "")

                if age_min <= MAX_AGE_MINUTES and _is_breaking_headline(headline, keywords, power_map):
                    breaking.append({
                        "headline": headline,
                        "source": article.get("source", "Unknown"),
                        "url": article.get("url", "#")
                    })
        else:
            for symbol in symbols:
                raw_rss = await fetch_yahoo_news(symbol)
                lines = raw_rss.lower().splitlines()
                if any(_is_breaking_headline(line, keywords, power_map) for line in lines):
                    breaking.append({
                        "headline": f"Significant Event for {symbol}",
                        "source": "Yahoo RSS",
                        "url": f"https://finance.yahoo.com/quote/{symbol}"
                    })

    except Exception as e:
        logger.error(f"❌ [News Engine] Detection failed: {e}")

    return breaking

# === Power Scoring Logic ===
def _is_breaking_headline(headline: str, keywords: list, power_map: dict) -> bool:
    score = 0
    lower = headline.lower()

    for word in keywords:
        if word in lower:
            base = 4
            bonus = power_map.get(word, 0) * 0.5
            score += base + bonus

    logger.debug(f"[News Scoring] {headline} → Score: {score:.2f}")
    return score >= POWER_THRESHOLD

# === Telegram Formatter ===
async def format_breaking_news(news_list: list, lang: str = "en") -> str:
    if not news_list:
        return ""

    header = {
        "en": "📰 *Breaking News Detected!*",
        "de": "📰 *Breaking News erkannt!*"
    }.get(lang, "📰 *Breaking News!*")

    footer = {
        "en": "_Markets react fast. Stay sharp._",
        "de": "_Märkte reagieren blitzschnell. Bleib wachsam._"
    }.get(lang, "_Stay alert._")

    formatted = [header]

    for news in news_list:
        headline = news.get("headline", "No headline")
        source = news.get("source", "Unknown")
        url = news.get("url", "#")

        formatted.append(
            f"• *{headline}*\n_Source: {source}_\n[More Details]({url})"
        )

    formatted.append(footer)
    return "\n\n".join(formatted)
