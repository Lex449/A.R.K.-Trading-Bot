# bot/utils/market_time.py

from datetime import datetime

def is_trading_day() -> bool:
    """
    Überprüft, ob heute ein normaler Handelstag ist (Montag-Freitag).
    Wochenende wird ausgeschlossen.
    """
    today = datetime.utcnow().weekday()  # 0 = Montag, 6 = Sonntag
    return today in [0, 1, 2, 3, 4]  # Nur Montag bis Freitag aktiv
