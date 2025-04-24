# bot/config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    return {
        # Telegram Konfiguration
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),

        # Finnhub API
        "FINNHUB_API_KEY": os.getenv("FINNHUB_API_KEY"),

        # Symbol-Map für Finnhub + Yahoo-kompatibel
        "SYMBOLS": {
            "US100": "^NDX",
            "US30": "^DJI",
            "SPX500": "^GSPC",
            "IWM": "IWM",
            "QQQ": "QQQ",
            "DIA": "DIA",
            "MDY": "MDY"
        },

        # Technische Indikatoren & Intervalle
        "INTERVAL": os.getenv("INTERVAL", "1m"),  # 1-Minuten-Intervall für Echtzeit
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),

        # Autosignal-Konfiguration (voll ausgelastet!)
        "AUTO_SIGNAL_SYMBOLS": os.getenv("AUTO_SIGNAL_SYMBOLS", "US100,US30,SPX500,IWM,QQQ,DIA,MDY").split(","),
        "AUTO_SIGNAL_INTERVAL": int(os.getenv("AUTO_SIGNAL_INTERVAL", 60)),   # Check alle 60 Sek.
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),  # ebenfalls 60 Sek.
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 9000)),  # volle 150 pro Minute!
    }
