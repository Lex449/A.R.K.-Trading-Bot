"""
A.R.K. Market Time Handler – Ultra Premium Trading Session Management 2025.
Handles NYSE/Nasdaq session detection including Pre-Market Warnings and US public holidays.

Built for: Precision Timing, Smart Session Control, API Load Efficiency.
Made in Bali. Engineered with German Precision.
"""

from datetime import datetime, time
import pytz
import holidays
from bot.utils.logger import setup_logger

# === Logger Setup ===
logger = setup_logger(__name__)

# === US Market Timezone (New York) ===
NY_TZ = pytz.timezone("America/New_York")

# === US Public Holidays ===
US_HOLIDAYS = holidays.US()

# === Trading Session Times (NYSE / NASDAQ) ===
MARKET_OPEN = time(9, 30)
MARKET_CLOSE = time(16, 0)
PREMARKET_WARNING_START = time(9, 15)

def get_now_est() -> datetime:
    """
    Returns the current datetime in US Eastern Time (New York).
    """
    return datetime.now(NY_TZ)

def is_trading_day(now: datetime = None) -> bool:
    """
    Checks if the current day is a valid trading day (Mon–Fri, not a US holiday).
    """
    now = now or get_now_est()
    is_weekday = now.weekday() < 5
    is_not_holiday = now.date() not in US_HOLIDAYS

    result = is_weekday and is_not_holiday
    logger.debug(f"[MarketTime] Trading Day: {result} | {now.strftime('%A %Y-%m-%d')}")
    return result

def is_trading_hours(now: datetime = None) -> bool:
    """
    Checks if the current NY time is between 9:30 and 16:00.
    """
    now = now or get_now_est()
    current_time = now.time()

    result = MARKET_OPEN <= current_time <= MARKET_CLOSE
    logger.debug(f"[MarketTime] Trading Hours: {result} | {current_time}")
    return result

def is_pre_market_open_warning(now: datetime = None) -> bool:
    """
    Checks if current NY time is between 9:15 and 9:30 (pre-open warning window).
    """
    now = now or get_now_est()
    current_time = now.time()

    result = PREMARKET_WARNING_START <= current_time < MARKET_OPEN
    if result:
        logger.info(f"⚠️ [MarketTime] Pre-Market Warning Active: {current_time}")
    return result

def get_market_status(now: datetime = None) -> str:
    """
    Returns human-readable market status.
    """
    now = now or get_now_est()

    if not is_trading_day(now):
        return "closed (Holiday or Weekend)"
    if is_trading_hours(now):
        return "open"
    if is_pre_market_open_warning(now):
        return "pre-market warning"
    return "closed (Outside Trading Hours)"
