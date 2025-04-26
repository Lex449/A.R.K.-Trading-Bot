# bot/utils/market_time.py

"""
Handles US trading session detection.
Optimized for NYSE/Nasdaq operating hours and US public holidays.
"""

from datetime import datetime, time
import pytz
import holidays
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# US public holidays
us_holidays = holidays.US()

def is_trading_day() -> bool:
    """
    Checks if today is a valid US trading day (Monday–Friday and not a public holiday).

    Returns:
        bool: True if it's a trading day, otherwise False.
    """
    now = datetime.now(pytz.timezone('America/New_York'))
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday
    today = now.date()

    if weekday in [0, 1, 2, 3, 4] and today not in us_holidays:
        logger.debug(f"Trading Day Check: ✅ {now.strftime('%A %Y-%m-%d')}")
        return True
    else:
        logger.debug(f"Trading Day Check: ❌ {now.strftime('%A %Y-%m-%d')}")
        return False

def is_trading_hours() -> bool:
    """
    Checks if current time is within NYSE/Nasdaq trading hours: 9:30 AM - 4:00 PM New York time.

    Returns:
        bool: True if market is open, otherwise False.
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    market_open = time(9, 30)
    market_close = time(16, 0)

    if market_open <= now <= market_close:
        logger.debug(f"Trading Hours Check: ✅ Now {now}")
        return True
    else:
        logger.debug(f"Trading Hours Check: ❌ Now {now}")
        return False

def is_pre_market_open_warning() -> bool:
    """
    Warns 15 minutes before NYSE opens (09:15 - 09:30 New York time).

    Returns:
        bool: True if inside warning window.
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    warning_start = time(9, 15)
    market_open = time(9, 30)

    if warning_start <= now < market_open:
        logger.info(f"Pre-Market Warning active: {now}")
        return True
    else:
        return False
