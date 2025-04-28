# bot/engine/news_alert_engine.py

"""
A.R.K. News Alert Engine – Breaking News Detector with Backup Source.
Fetches and analyzes market news from Finnhub or Yahoo Finance if needed.
"""

import aiohttp
import asyncio
from datetime import datetime
from bot.config.settings import get_settings
from bot.utils.news_health_checker import use_finnhub

# Load configuration
config = get_settings()
finnhub_api_key = config.get("FINNHUB_API_KEY")
symbols = config.get("AUTO_SIGNAL_SYMBOLS", [])

# Endpoints
FINNHUB_ENDPOINT = f"https://finnhub.io/api/v1/news?category=general&token={finnhub_api_key}"
YAHOO_ENDPOINT_TEMPLATE = "https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"

important_keywords = [
    "inflation", "rate hike", "recession", "crash", "bankruptcy",
    "fed", "layoffs", "defaults", "market turmoil", "collapse",
    "interest rates", "geopolitical", "fomc", "earnings warning"
]

async def fetch_finnhub_news() -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get(FINNHUB_ENDPOINT, timeout=10) as response:
            if response.status == 200:
                return await response.json()
            return []

async def fetch_yahoo_news(symbol: str) -> list:
    try:
        async with aiohttp.ClientSession() as session:
            url = YAHOO_ENDPOINT_TEMPLATE.format(symbol=symbol)
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
            return ""
    except Exception:
        return ""

async def detect_breaking_news() -> list:
    breaking_news = []

    if use_finnhub():
        news_list = await fetch_finnhub_news()
        now = datetime.utcnow()
        for article in news_list:
            try:
                published_time = datetime.utcfromtimestamp(article.get("datetime", 0))
                if (now - published_time).total_seconds() / 60 > 15:
                    continue
                headline = article.get("headline", "").lower()
                if any(keyword in headline for keyword in important_keywords):
                    breaking_news.append({
                        "headline": article.get("headline", ""),
                        "source": article.get("source", "unknown"),
                        "url": article.get("url", "")
                    })
            except Exception:
                continue
    else:
        for symbol in symbols:
            raw_rss = await fetch_yahoo_news(symbol)
            if any(keyword in raw_rss.lower() for keyword in important_keywords):
                breaking_news.append({
                    "headline": f"Potential Breaking News detected for {symbol}",
                    "source": "Yahoo Finance RSS",
                    "url": f"https://finance.yahoo.com/quote/{symbol}"
                })
    return breaking_news

async def format_breaking_news(news_list: list, lang: str = "en") -> str:
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
        headline = news.get("headline", "")
        source = news.get("source", "Unknown")
        url = news.get("url", "")

        parts.append(f"• *{headline}*\nSource: {source}\n[Details]({url})")

    parts.append(footer)
    return "\n\n".join(parts)
