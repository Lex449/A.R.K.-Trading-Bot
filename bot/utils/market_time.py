# bot/utils/market_time.py

from datetime import datetime, time
import pytz
import holidays
import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# US Feiertage vorbereiten
us_holidays = holidays.US()

def is_trading_day() -> bool:
    """
    Check if today is a US trading day (Monday–Friday and not a public holiday).
    
    Returns:
        bool: True if it's a trading day, False if weekend or US holiday.
    """
    now = datetime.now(pytz.timezone('America/New_York'))
    weekday = now.weekday()  # 0 = Monday, 6 = Sunday
    today_date = now.date()

    if weekday not in [0, 1, 2, 3, 4]:
        logger.info(f"Today is weekend ({today_date}). Markets are closed.")
        return False

    if today_date in us_holidays:
        logger.info(f"Today is a public US holiday ({today_date}). Markets are closed.")
        return False

    logger.info(f"Today ({today_date}) is a trading day.")
    return True

def is_trading_hours() -> bool:
    """
    Check if current time is within regular US stock market hours.
    NYSE/Nasdaq: 9:30 AM to 4:00 PM New York time.
    
    Returns:
        bool: True if within market hours, False otherwise.
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    market_open = time(9, 30)
    market_close = time(16, 0)

    if market_open <= now <= market_close:
        logger.info("We are within US trading hours.")
        return True
    else:
        logger.info("We are outside US trading hours.")
        return False
