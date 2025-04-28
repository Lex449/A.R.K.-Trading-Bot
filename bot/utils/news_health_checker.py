# bot/utils/news_health_checker.py

"""
A.R.K. News Health Checker – Primary vs Backup Source Manager.
Ensures real-time switching between Finnhub and Yahoo Finance News feeds.
"""

import aiohttp
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Global State
_finnhub_available = True

async def check_finnhub_health(timeout_sec: int = 5) -> bool:
    """
    Checks if Finnhub News API is available.

    Args:
        timeout_sec (int): Timeout for health check request.

    Returns:
        bool: True if Finnhub is healthy, False otherwise.
    """
    global _finnhub_available

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://finnhub.io/api/v1/news?category=general", timeout=timeout_sec) as response:
                if response.status == 200:
                    if not _finnhub_available:
                        logger.info("✅ [News Health] Finnhub news source restored.")
                    _finnhub_available = True
                    return True
                else:
                    logger.warning(f"⚠️ [News Health] Finnhub returned status {response.status}.")
                    _finnhub_available = False
                    return False
    except Exception as error:
        logger.error(f"❌ [News Health] Finnhub unreachable: {error}")
        _finnhub_available = False
        return False

def use_finnhub() -> bool:
    """
    Returns whether Finnhub should be used as the primary news source.

    Returns:
        bool: True if Finnhub is healthy, False otherwise.
    """
    return _finnhub_available
