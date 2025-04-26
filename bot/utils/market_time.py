# bot/utils/market_time.py

from datetime import datetime, time

def is_trading_day_and_time() -> bool:
    """
    Prüft, ob heute ein US-Handelstag (Mo-Fr) ist UND ob die aktuelle UTC-Zeit
    innerhalb der regulären Handelszeiten liegt (13:30 bis 20:00 UTC für NYSE/Nasdaq).
    """

    now = datetime.utcnow()
    weekday = now.weekday()  # 0 = Montag, 6 = Sonntag

    # Check: Nur Montag bis Freitag
    if weekday > 4:
        return False

    # Check: Nur zwischen 13:30 und 20:00 UTC
    market_open = time(13, 30)
    market_close = time(20, 0)

    if market_open <= now.time() <= market_close:
        return True

    return False
