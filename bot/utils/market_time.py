# bot/utils/market_time.py

"""
A.R.K. Market Time Handler – Trading Session Management.
Handles US trading session detection based on NYSE/Nasdaq hours and US public holidays.
"""

from datetime import datetime, time
import pytz
import holidays
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# US public holidays (dynamic)
us_holidays = holidays.US()

def is_trading_day() -> bool:
    """
    Checks if today is a valid US trading day.
    - Monday to Friday
    - Not a US public holiday

    Returns:
        bool: True if it's a trading day, otherwise False.
    """
    now = datetime.now(pytz.timezone('America/New_York'))
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday
    today = now.date()

    if weekday in [0, 1, 2, 3, 4] and today not in us_holidays:
        logger.debug(f"✅ [Market Time] Trading Day: {now.strftime('%A %Y-%m-%d')}")
        return True
    else:
        logger.debug(f"❌ [Market Time] Not a Trading Day: {now.strftime('%A %Y-%m-%d')}")
        return False

def is_trading_hours() -> bool:
    """
    Checks if the current time is within regular NYSE/Nasdaq trading hours (09:30 - 16:00 ET).

    Returns:
        bool: True if inside trading hours, otherwise False.
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    market_open = time(9, 30)
    market_close = time(16, 0)

    if market_open <= now <= market_close:
        logger.debug(f"✅ [Market Time] Trading Hours: {now}")
        return True
    else:
        logger.debug(f"❌ [Market Time] Outside Trading Hours: {now}")
        return False

def is_pre_market_open_warning() -> bool:
    """
    Checks if within the 15-minute warning window before NYSE opens (09:15 - 09:30 ET).

    Returns:
        bool: True if in pre-market warning window, otherwise False.
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    warning_start = time(9, 15)
    market_open = time(9, 30)

    if warning_start <= now < market_open:
        logger.info(f"⚠️ [Market Time] Pre-Market Warning Active: {now}")
        return True
    else:
        return False
