"""
A.R.K. News Health Checker – Ultra Premium Stability Build 4.0
Real-time monitoring and dynamic switching between Finnhub and Yahoo Finance based on service health.

Built for: Fault Tolerance, Lightning Recovery, and 24/7 Signal Reliability.
Made in Bali. Engineered with German Precision.
"""

import aiohttp
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# === Setup Logger and Config ===
logger = setup_logger(__name__)
config = get_settings()

# === Constants ===
FINNHUB_API_KEY = config.get("FINNHUB_API_KEY")
FINNHUB_ENDPOINT = f"https://finnhub.io/api/v1/news?category=general&token={FINNHUB_API_KEY}"

# === Global Health State ===
_finnhub_healthy = True

def use_finnhub() -> bool:
    """
    Determines whether Finnhub should be used as the active news source.

    Returns:
        bool: True if Finnhub is healthy, False if fallback (Yahoo Finance) is active.
    """
    return _finnhub_healthy

async def check_finnhub_health(timeout_sec: int = 5) -> None:
    """
    Pings Finnhub API to verify availability.
    Updates internal status and triggers source switching if necessary.

    Args:
        timeout_sec (int): Timeout for the API health check.
    """
    global _finnhub_healthy

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(FINNHUB_ENDPOINT, timeout=timeout_sec) as response:
                if response.status == 200:
                    if not _finnhub_healthy:
                        logger.info("✅ [News Health] Finnhub API back online. Switching primary source to Finnhub.")
                    _finnhub_healthy = True
                else:
                    if _finnhub_healthy:
                        logger.warning(f"⚠️ [News Health] Finnhub error {response.status}. Switching to Yahoo Finance.")
                    _finnhub_healthy = False

    except Exception as e:
        if _finnhub_healthy:
            logger.error(f"❌ [News Health] Finnhub unavailable: {e}. Switching to Yahoo Finance fallback.")
        _finnhub_healthy = False
