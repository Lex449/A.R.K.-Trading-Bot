# bot/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    return {
        # Telegram Konfiguration
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),

        # Analyse-Konfiguration
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),
        "INTERVAL": os.getenv("INTERVAL", "1min"),

        # Signal-Konfiguration
        "AUTO_SIGNAL_SYMBOLS": [s.strip() for s in os.getenv("AUTO_SIGNAL_SYMBOLS", "").split(",") if s.strip()],
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 150)),

        # TwelveData API Key
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY")
    }
