# bot/config/config.py
# Konfigurationsdatei für den Trading-Bot
# Hier werden API-Schlüssel, Tokens und andere Einstellungen hinterlegt.

# Telegram-Bot Token (von BotFather bereitgestellt)
TELEGRAM_TOKEN = "7859748584:AAHNOoN9v7X8mrDOxHik8fOXZgyc3efGC5I"

# TwelveData API-Schlüssel für Marktdaten
TWELVEDATA_API_KEY = "Odd4ddf44b144ea48df01c9f-dfc80921"

# Zu überwachende Indizes und ihre jeweiligen Symbols für TwelveData
# US100 -> Nasdaq-100, US30 -> Dow Jones 30, US500 -> S&P 500
SYMBOLS = {
    "US100": "NDX",   # Nasdaq-100 Index
    "US30": "DJI",    # Dow Jones Industrial Average
    "US500": "SPX"    # S&P 500 Index
}

# Intervall für die technischen Analysen (z.B. "5min", "15min", etc.)
INTERVAL = "5min"

# Einstellungen für technische Indikatoren
RSI_PERIOD = 14         # Zeitraum für RSI-Berechnung
EMA_SHORT_PERIOD = 20   # Kürzerer EMA für Trendanalyse
EMA_LONG_PERIOD = 50    # Längerer EMA für Trendanalyse

# Sonstige Einstellungen
SIGNAL_CHECK_INTERVAL_SEC = 300  # Interval in Sekunden für automatische Signalprüfung (300s = 5min)
