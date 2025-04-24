# bot/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
        "FINNHUB_API_KEY": os.getenv("FINNHUB_API_KEY"),

        "SYMBOLS": {
            "US100": "^NDX",
            "US30": "^DJI",
            "SPX500": "^GSPC",
            "DE40": "^GDAXI",
            "JP225": "^N225",
            "HK50": "^HSI"
        },

        "INTERVAL": os.getenv("INTERVAL", "1m"),
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),

        "AUTO_SIGNAL_SYMBOLS": os.getenv("AUTO_SIGNAL_SYMBOLS", "US100,US30,SPX500,DE40,JP225,HK50").split(","),
        "AUTO_SIGNAL_INTERVAL": int(os.getenv("AUTO_SIGNAL_INTERVAL", 90)),
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 8)),
    }
