"""
A.R.K. Market Session Guard – Ultra Precision US Market Timer.
Prevents unnecessary analysis and trading outside active US trading hours.

Built for: Efficiency, API Protection, Maximum Signal Quality.
"""

from datetime import datetime, time
import pytz

# New York timezone for US market
NEW_YORK_TZ = pytz.timezone("America/New_York")

def is_us_market_open() -> bool:
    """
    Checks if the US stock market is currently open.

    US Market Hours:
    - Monday to Friday
    - 09:30 AM to 04:00 PM (New York Time)

    Returns:
        bool: True if market is open, False otherwise.
    """
    now_ny = datetime.now(NEW_YORK_TZ)
    current_time = now_ny.time()

    is_weekday = now_ny.weekday() < 5  # 0 = Monday, 4 = Friday
    market_open = time(9, 30)
    market_close = time(16, 0)

    return is_weekday and market_open <= current_time <= market_close

def minutes_until_market_open() -> int:
    """
    Calculates minutes remaining until US market opens.

    Useful for pre-open reminders.

    Returns:
        int: Minutes until open (negative if already open).
    """
    now_ny = datetime.now(NEW_YORK_TZ)
    market_open = now_ny.replace(hour=9, minute=30, second=0, microsecond=0)

    delta = (market_open - now_ny).total_seconds() / 60  # Minutes
    return int(delta)
