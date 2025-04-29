# bot/utils/market_time.py

"""
A.R.K. Market Time Handler – Ultra Premium Trading Session Management 2025.
Handles NYSE/Nasdaq session detection including Pre-Market Warnings and US public holidays.
"""

from datetime import datetime, time
import pytz
import holidays
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# US Holidays
us_holidays = holidays.US()

# Timezone for US Markets (New York Time)
NY_TIMEZONE = pytz.timezone('America/New_York')

def get_now_est() -> datetime:
    """
    Returns the current datetime in US Eastern Time (New York).
    """
    return datetime.now(NY_TIMEZONE)

def is_trading_day(now: datetime = None) -> bool:
    """
    Checks if today is a US trading day (Monday-Friday and not a US holiday).

    Args:
        now (datetime, optional): Specific time for testing, otherwise current.

    Returns:
        bool: True if it is a trading day, False otherwise.
    """
    now = now or get_now_est()
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday
    today = now.date()

    if weekday < 5 and today not in us_holidays:
        logger.debug(f"✅ [MarketTime] Trading Day detected: {now.strftime('%A %Y-%m-%d')}")
        return True
    else:
        logger.debug(f"❌ [MarketTime] Non-Trading Day: {now.strftime('%A %Y-%m-%d')}")
        return False

def is_trading_hours(now: datetime = None) -> bool:
    """
    Checks if the current time is within normal US trading hours (9:30 - 16:00 ET).

    Args:
        now (datetime, optional): Specific time for testing.

    Returns:
        bool: True if inside trading hours, False otherwise.
    """
    now = now or get_now_est().time()
    market_open = time(9, 30)
    market_close = time(16, 0)

    if market_open <= now <= market_close:
        logger.debug(f"✅ [MarketTime] Within Trading Hours: {now}")
        return True
    else:
        logger.debug(f"❌ [MarketTime] Outside Trading Hours: {now}")
        return False

def is_pre_market_open_warning(now: datetime = None) -> bool:
    """
    Checks if we are within the 15-minute Pre-Market window before NYSE opens.

    Args:
        now (datetime, optional): Specific time for testing.

    Returns:
        bool: True if within 9:15 - 9:30 ET window.
    """
    now = now or get_now_est().time()
    warning_start = time(9, 15)
    market_open = time(9, 30)

    if warning_start <= now < market_open:
        logger.info(f"⚠️ [MarketTime] Pre-Market Warning Active: {now}")
        return True
    else:
        return False

def get_market_status() -> str:
    """
    Returns the full market status ("open", "closed", "pre-market-warning").

    Returns:
        str: Status text
    """
    now = get_now_est()

    if not is_trading_day(now):
        return "closed (Holiday/Weekend)"
    if is_pre_market_open_warning(now):
        return "pre-market warning"
    if is_trading_hours(now):
        return "open"
    return "closed (Outside Trading Hours)"
