"""
A.R.K. News Health Checker – Ultra Premium Stability Build.
Real-time monitoring and switching between Finnhub and Yahoo Finance news sources.
"""

import aiohttp
import logging
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# === Setup ===
logger = setup_logger(__name__)
config = get_settings()

# Constants
FINNHUB_API_KEY = config.get("FINNHUB_API_KEY")
FINNHUB_ENDPOINT = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"

# Global State
_finnhub_available = True

def use_finnhub() -> bool:
    """
    Returns whether Finnhub should be used as the primary news source.

    Returns:
        bool: True if Finnhub is healthy, False if fallback (Yahoo) needed.
    """
    return _finnhub_available

async def check_finnhub_health(timeout_sec: int = 5):
    """
    Checks if Finnhub News API is currently healthy.
    Automatically switches backup source if needed.

    Args:
        timeout_sec (int): Timeout duration for health check request.

    Returns:
        None
    """
    global _finnhub_available

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FINNHUB_ENDPOINT, timeout=timeout_sec) as response:
                if response.status == 200:
                    if not _finnhub_available:
                        logger.info("✅ [News Health] Finnhub connection restored. Using Finnhub again.")
                    _finnhub_available = True
                else:
                    if _finnhub_available:
                        logger.warning(f"⚠️ [News Health] Finnhub returned status {response.status}. Switching to backup.")
                    _finnhub_available = False

    except Exception as e:
        if _finnhub_available:
            logger.error(f"❌ [News Health] Finnhub unreachable: {e}. Switching to backup source.")
        _finnhub_available = False
