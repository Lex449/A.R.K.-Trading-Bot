# bot/utils/holiday_checker.py

from datetime import datetime

# Liste der wichtigsten US-Feiertage (Monat, Tag)
US_MARKET_HOLIDAYS = [
    (1, 1),    # Neujahr
    (7, 4),    # Independence Day
    (12, 25),  # Weihnachten
    (11, 23),  # Thanksgiving (annähernd, vereinfacht)
    (1, 15),   # Martin Luther King Jr. Day (immer 3. Montag, hier als 15. pauschalisiert)
    (2, 19),   # Presidents' Day (3. Montag im Februar, vereinfacht)
    (5, 27),   # Memorial Day (letzter Montag im Mai, ca. 27.)
    (9, 2),    # Labor Day (erster Montag im September, ca. 2.)
]

def is_us_holiday() -> bool:
    """
    Checks if today is a recognized US stock market holiday.

    Returns:
        bool: True if today is a holiday, False otherwise.
    """
    today = datetime.utcnow()
    today_tuple = (today.month, today.day)

    if today_tuple in US_MARKET_HOLIDAYS:
        return True
    return False
