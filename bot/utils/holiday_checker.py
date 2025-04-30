"""
A.R.K. Holiday Checker – Smart Market Pause Detection 2025.
Detects fixed and approximated US stock market holidays.

Built for: API Protection, Efficiency Boost, Market-Aware Execution.
Made in Bali. Engineered with German Precision.
"""

from datetime import datetime
import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Static Approximation of Major US Holidays ===
US_MARKET_HOLIDAYS = {
    (1, 1): "New Year's Day",
    (1, 15): "Martin Luther King Jr. Day",
    (2, 19): "Presidents' Day",
    (5, 27): "Memorial Day",
    (7, 4): "Independence Day",
    (9, 2): "Labor Day",
    (11, 23): "Thanksgiving Day",
    (12, 25): "Christmas Day"
}

def is_us_holiday(now: datetime = None) -> bool:
    """
    Checks if today matches one of the known US stock market holidays.

    Args:
        now (datetime, optional): Custom datetime (UTC). Defaults to now.

    Returns:
        bool: True if today is a holiday.
    """
    now = now or datetime.utcnow()
    today_tuple = (now.month, now.day)

    if today_tuple in US_MARKET_HOLIDAYS:
        holiday_name = US_MARKET_HOLIDAYS[today_tuple]
        logger.info(f"🛑 [HolidayChecker] Holiday Detected: {holiday_name} ({today_tuple})")
        return True

    logger.debug(f"✅ [HolidayChecker] No holiday today: {today_tuple}")
    return False
