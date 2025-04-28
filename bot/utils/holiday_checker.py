# bot/utils/holiday_checker.py

"""
A.R.K. Holiday Checker – Smart Market Pause Detection.
Checks if today is a US stock market holiday (static approximation).
"""

from datetime import datetime
import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Key US market holidays (static approximation for basic use)
US_MARKET_HOLIDAYS = [
    (1, 1),    # New Year's Day (Fixed)
    (1, 15),   # Martin Luther King Jr. Day (Approximated as Jan 15)
    (2, 19),   # Presidents' Day (Approximated as Feb 19)
    (5, 27),   # Memorial Day (Approximated as May 27)
    (7, 4),    # Independence Day (Fixed)
    (9, 2),    # Labor Day (Approximated as Sep 2)
    (11, 23),  # Thanksgiving Day (Approximated as Nov 23)
    (12, 25),  # Christmas Day (Fixed)
]

def is_us_holiday() -> bool:
    """
    Determines if today matches a static US stock market holiday.

    Returns:
        bool: True if today is considered a holiday, False otherwise.
    """
    today = datetime.utcnow()
    today_tuple = (today.month, today.day)

    if today_tuple in US_MARKET_HOLIDAYS:
        logger.info(f"🛑 [Holiday Checker] Market closed today: {today_tuple}")
        return True
    else:
        logger.debug(f"✅ [Holiday Checker] No holiday today: {today_tuple}")
        return False
