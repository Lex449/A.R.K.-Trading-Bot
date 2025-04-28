# bot/utils/news_health_checker.py

"""
A.R.K. News Health Checker – Primary vs Backup Source Manager.
Ensures real-time switching between Finnhub and Yahoo Finance News feeds.
"""

import aiohttp
import asyncio
import logging

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Global State
_finnhub_available = True

async def check_finnhub_health() -> bool:
    """
    Checks if Finnhub News API is available.

    Returns:
        bool: True if Finnhub is healthy, False otherwise.
    """
    global _finnhub_available
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://finnhub.io/api/v1/news?category=general", timeout=5) as response:
                if response.status == 200:
                    if not _finnhub_available:
                        logger.info("✅ Finnhub primary news source restored.")
                    _finnhub_available = True
                    return True
                else:
                    logger.warning("⚠️ Finnhub news service responded with non-200 status.")
                    _finnhub_available = False
                    return False
    except Exception:
        logger.error("❌ Finnhub news service unreachable. Switching to Yahoo backup.")
        _finnhub_available = False
        return False

def use_finnhub() -> bool:
    """
    Returns whether Finnhub should be used as primary news source.
    """
    return _finnhub_available
