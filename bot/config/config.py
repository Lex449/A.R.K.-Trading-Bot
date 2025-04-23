# bot/config/config.py

import os
from dotenv import load_dotenv

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Telegram-Bot Token (vom BotFather bereitgestellt)
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")  # Lädt den Token aus der .env-Datei

# TwelveData API-Schlüssel für Marktdaten
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")  # Lädt den TwelveData API-Schlüssel aus der .env-Datei

# Zu überwachende Indizes und ihre Symbole für TwelveData
SYMBOLS = {
    "US100": "NDX",  # Nasdaq-100 Index
    "US30": "DJI",   # Dow Jones Industrial Average
    "US500": "SPX",   # S&P 500 Index
}

# Intervall für die technischen Analysen (z.B. "5min", "15min", etc.)
INTERVAL = "5min"

# Einstellungen für technische Indikatoren
RSI_PERIOD = 14          # Zeitraum für RSI-Berechnung
EMA_SHORT_PERIOD = 20    # Kürzerer EMA für Trendanalyse
EMA_LONG_PERIOD = 50     # Längerer EMA für Trendanalyse

# Sonstige Einstellungen
SIGNAL_CHECK_INTERVAL_SEC = 300  # Interval in Sekunden für automatische Signalprüfung (300s = 5min)
MAX_SIGNALS_PER_HOUR = 10        # Maximal erlaubte Signale pro Stunde (z.B. für Spam-Prevention)
