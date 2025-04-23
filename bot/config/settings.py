import os
from dotenv import load_dotenv

# Lade Umgebungsvariablen aus der .env-Datei
load_dotenv()

def get_settings():
    """Lädt alle nötigen Konfigurationen und gibt sie als Dictionary zurück."""
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),  # Telegram Bot Token
        "DANIEL_TELEGRAM_ID": os.getenv("DANIEL_TELEGRAM_ID"),  # Deine Telegram-ID
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY"),  # API-Schlüssel für TwelveData
        "SYMBOLS": {
            "US100": "NDX",  # Nasdaq-100
            "US30": "DJI",   # Dow Jones Industrial Average
            "US500": "SPX"    # S&P 500
        },
        "INTERVAL": os.getenv("INTERVAL", "5min"),  # Standard-Intervall auf "5min", wenn nicht anders gesetzt
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),  # Standard RSI-Periode auf 14 setzen
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 20)),  # Standard EMA-short-Periode auf 20
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 50)),  # Standard EMA-long-Periode auf 50
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 300)),  # Default auf 5 Minuten (300 Sekunden)
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 10))  # Maximal 10 Signale pro Stunde
    }
