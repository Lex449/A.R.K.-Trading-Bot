# bot/utils/market_time.py

from datetime import datetime, time
import pytz

def is_trading_day() -> bool:
    """
    Check if today is a normal US trading day (Monday to Friday).
    """
    today = datetime.now(pytz.timezone('America/New_York')).weekday()  # 0 = Monday, 6 = Sunday
    return today in [0, 1, 2, 3, 4]  # Only Monday to Friday

def is_trading_hours() -> bool:
    """
    Check if current time is within US stock market trading hours.
    NYSE/Nasdaq regular trading hours: 9:30 AM to 4:00 PM New York time.
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    market_open = time(9, 30)  # 9:30 AM
    market_close = time(16, 0)  # 4:00 PM

    return market_open <= now <= market_close
