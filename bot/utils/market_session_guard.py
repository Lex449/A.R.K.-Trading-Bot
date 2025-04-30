"""
A.R.K. Market Session Guard – Ultra Precision US Market Timer.
Prevents unnecessary analysis and trading outside active US trading hours.

Built for: Efficiency, API Protection, Maximum Signal Quality.
Made in Bali. Engineered with German Precision.
"""

from datetime import datetime, time, timedelta
import pytz
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Timezone definition
NEW_YORK_TZ = pytz.timezone("America/New_York")

# US Stock Market Trading Hours
MARKET_OPEN = time(9, 30)
MARKET_CLOSE = time(16, 0)

# Optional – add public holidays here (format: YYYY-MM-DD)
US_MARKET_HOLIDAYS = {
    "2025-01-01",  # New Year's Day
    "2025-01-20",  # Martin Luther King Jr. Day
    "2025-02-17",  # Presidents' Day
    "2025-04-18",  # Good Friday
    "2025-05-26",  # Memorial Day
    "2025-07-04",  # Independence Day
    "2025-09-01",  # Labor Day
    "2025-11-27",  # Thanksgiving Day
    "2025-12-25",  # Christmas Day
}

def is_us_market_open() -> bool:
    """
    Returns True if current time in New York is within US trading hours.
    Excludes weekends and optional US holidays.
    """
    now_ny = datetime.now(NEW_YORK_TZ)
    today_str = now_ny.strftime("%Y-%m-%d")

    is_weekday = now_ny.weekday() < 5  # Monday–Friday
    is_not_holiday = today_str not in US_MARKET_HOLIDAYS
    is_open_time = MARKET_OPEN <= now_ny.time() <= MARKET_CLOSE

    market_status = is_weekday and is_not_holiday and is_open_time
    logger.debug(f"[SessionGuard] Market check → {market_status} | {now_ny.time()} NY Time")

    return market_status

def minutes_until_market_open() -> int:
    """
    Returns minutes remaining until market open (negative if already open).
    """
    now_ny = datetime.now(NEW_YORK_TZ)
    today_open = now_ny.replace(hour=9, minute=30, second=0, microsecond=0)

    delta = (today_open - now_ny).total_seconds() / 60
    logger.debug(f"[SessionGuard] Minutes until open: {delta:.1f}")
    return int(delta)

def next_market_open_time() -> str:
    """
    Returns the next expected US market opening time in readable format.
    """
    now_ny = datetime.now(NEW_YORK_TZ)
    weekday = now_ny.weekday()

    # If market is still opening today
    if weekday < 5 and now_ny.time() < MARKET_OPEN:
        next_open = now_ny.replace(hour=9, minute=30, second=0, microsecond=0)
    else:
        # Go to next weekday (skip weekends)
        next_day = now_ny + timedelta(days=1)
        while next_day.weekday() >= 5:
            next_day += timedelta(days=1)
        next_open = next_day.replace(hour=9, minute=30, second=0, microsecond=0)

    return next_open.strftime("%A %Y-%m-%d %H:%M NY Time")
