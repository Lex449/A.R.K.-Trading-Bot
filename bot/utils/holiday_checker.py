# bot/utils/holiday_checker.py

"""
Checks if today is a US stock market holiday.
Designed for fast pre-checks before data polling or trading logic.
"""

from datetime import datetime
import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Key US market holidays (static approximation)
US_MARKET_HOLIDAYS = [
    (1, 1),    # New Year's Day
    (7, 4),    # Independence Day
    (12, 25),  # Christmas Day
    (11, 23),  # Thanksgiving (approximate)
    (1, 15),   # MLK Day (approximated as Jan 15)
    (2, 19),   # Presidents' Day (approximated as Feb 19)
    (5, 27),   # Memorial Day (approximate)
    (9, 2),    # Labor Day (approximate)
]

def is_us_holiday() -> bool:
    """
    Checks whether today is a (static) US stock market holiday.

    Returns:
        bool: True if today matches a holiday, False otherwise.
    """
    today = datetime.utcnow()
    today_tuple = (today.month, today.day)

    if today_tuple in US_MARKET_HOLIDAYS:
        logger.info(f"🛑 Today is a US holiday: {today_tuple}")
        return True
    else:
        logger.debug(f"✅ No holiday detected today: {today_tuple}")
        return False
