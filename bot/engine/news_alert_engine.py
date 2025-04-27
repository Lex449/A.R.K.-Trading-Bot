# bot/engine/news_alert_engine.py

"""
A.R.K. News Alert Engine – Breaking News Detector.
Fetches and analyzes market news for real-time alerts.

Engineered for: Crash Prevention, Smart Trading Adjustments.
"""

import aiohttp
import asyncio
from datetime import datetime, timedelta
from bot.config.settings import get_settings

# Load configuration
config = get_settings()
finnhub_api_key = config.get("FINNHUB_API_KEY")
language_default = config.get("BOT_LANGUAGE", "en")

NEWS_ENDPOINT = f"https://finnhub.io/api/v1/news?category=general&token={finnhub_api_key}"

async def fetch_latest_news() -> list:
    """
    Fetches the latest market news from Finnhub.

    Returns:
        list: List of news dictionaries.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(NEWS_ENDPOINT) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []

async def detect_breaking_news() -> list:
    """
    Detects major breaking news events.

    Returns:
        list: List of important news headlines.
    """
    news_list = await fetch_latest_news()
    breaking_news = []

    if not news_list:
        return breaking_news

    now = datetime.utcnow()
    max_age_minutes = 15

    for article in news_list:
        # Check if news is recent
        published_time = datetime.fromisoformat(article["datetime"].replace("Z", "+00:00"))
        age_minutes = (now - published_time).total_seconds() / 60

        if age_minutes > max_age_minutes:
            continue  # Skip old news

        # Check if headline contains important keywords
        headline = article.get("headline", "").lower()

        important_keywords = [
            "inflation", "cpi", "rate hike", "rate cut", "fed", "recession",
            "interest rate", "dow jones", "nasdaq", "sp500", "tech selloff", "bank collapse"
        ]

        if any(keyword in headline for keyword in important_keywords):
            breaking_news.append({
                "headline": article.get("headline", ""),
                "summary": article.get("summary", ""),
                "source": article.get("source", "unknown"),
                "url": article.get("url", "")
            })

    return breaking_news

async def format_breaking_news(news_list: list, lang: str = "en") -> str:
    """
    Formats a list of breaking news articles into a single message.

    Args:
        news_list (list): List of news articles.
        lang (str): "en" or "de"

    Returns:
        str: Formatted news alert message.
    """
    if not news_list:
        return ""

    if lang == "de":
        header = "📰 *Breaking News erkannt!*"
        footer = "\n_Aktuelle Nachrichten können den Markt erheblich beeinflussen._"
    else:
        header = "📰 *Breaking News Detected!*"
        footer = "\n_Current events may heavily impact the market._"

    parts = [header]

    for news in news_list:
        headline = news.get("headline", "")
        source = news.get("source", "Unknown")
        url = news.get("url", "")

        parts.append(f"• *{headline}*  \nSource: {source}  \n[Details]({url})")

    parts.append(footer)
    return "\n\n".join(parts)
