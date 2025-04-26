# bot/utils/market_time.py

from datetime import datetime, time
import pytz
import holidays

# US Feiertage
us_holidays = holidays.US()

def is_trading_day() -> bool:
    """
    Check if today is a US trading day (Monday–Friday and not a public holiday).
    """
    now = datetime.now(pytz.timezone('America/New_York'))
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday
    today_date = now.date()

    # Monday to Friday + not a public holiday
    return weekday in [0, 1, 2, 3, 4] and today_date not in us_holidays

def is_trading_hours() -> bool:
    """
    Check if current time is within regular US stock market hours.
    NYSE/Nasdaq: 9:30 AM to 4:00 PM New York time.
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    market_open = time(9, 30)
    market_close = time(16, 0)

    return market_open <= now <= market_close
