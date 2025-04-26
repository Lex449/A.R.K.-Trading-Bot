# bot/utils/market_time.py

from datetime import datetime, time
import pytz
import holidays

# Feiertage USA
us_holidays = holidays.US()

def is_trading_day() -> bool:
    """
    Checkt, ob heute ein normaler US-Handelstag ist (kein Wochenende, kein Feiertag).
    """
    now = datetime.now(pytz.timezone('America/New_York'))
    weekday = now.weekday()  # 0 = Montag (bis 4 = Freitag)
    today_date = now.date()

    return weekday in range(5) and today_date not in us_holidays

def is_trading_hours() -> bool:
    """
    Checkt, ob jetzt normale US-Handelszeiten sind (NYSE/Nasdaq).
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    return time(9, 30) <= now <= time(16, 0)

def is_15min_before_market_open() -> bool:
    """
    Checkt, ob wir uns 15 Minuten vor Marktöffnung befinden.
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    return time(9, 15) <= now < time(9, 30)

def is_15min_before_market_close() -> bool:
    """
    Checkt, ob wir uns 15 Minuten vor Marktschluss befinden.
    """
    now = datetime.now(pytz.timezone('America/New_York')).time()
    return time(15, 45) <= now < time(16, 0)

def is_friday_close() -> bool:
    """
    Checkt, ob es Freitag nach Handelsschluss ist (für Wochenabschluss-Message).
    """
    now = datetime.now(pytz.timezone('America/New_York'))
    return now.weekday() == 4 and now.time() > time(16, 0)
