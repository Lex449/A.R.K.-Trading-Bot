import os
from dotenv import load_dotenv

# ENV-Variablen lokal laden (nur für Replit, nicht Railway)
load_dotenv()

def get_settings():
    """Lädt alle Konfigurationen aus der .env bzw. Railway."""
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY"),

        "SYMBOLS": {
            "QQQ": "QQQ",
            "SPY": "SPY",
            "DIA": "DIA",
            "IWM": "IWM",
            "MDY": "MDY",
            "US100": "NDX",
            "US30": "DJI",
            "SPX500": "SPX",
            "DAX": "DAX"
        },

        "INTERVAL": os.getenv("INTERVAL", "5min"),
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 20)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 50)),

        "AUTO_SIGNAL_SYMBOLS": os.getenv("AUTO_SIGNAL_SYMBOLS", "US100,US30,SPX500,DAX").split(","),
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 10))
    }