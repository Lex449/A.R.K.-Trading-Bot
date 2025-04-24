# bot/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    return {
        # Telegram
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "DANIEL_TELEGRAM_ID": os.getenv("DANIEL_TELEGRAM_ID"),

        # Finnhub API
        "FINNHUB_API_KEY": os.getenv("FINNHUB_API_KEY"),

        # YFinance Backup (kein Key notwendig)
        "USE_YFINANCE": True,

        # Signal-Konfiguration
        "AUTO_SIGNAL_SYMBOLS": os.getenv("AUTO_SIGNAL_SYMBOLS", "US100,US30,DE40,JP225,HK50,SPX500").split(","),
        "AUTO_SIGNAL_INTERVAL": int(os.getenv("AUTO_SIGNAL_INTERVAL", 300)),
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 10)),

        # Indikatoren
        "INTERVAL": os.getenv("INTERVAL", "5min"),
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 20)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 50)),
    }
