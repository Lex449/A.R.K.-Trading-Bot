import os
from dotenv import load_dotenv

# ENV nur lokal laden (auf Railway ignoriert)
load_dotenv()

def get_settings():
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY"),

        # Märkte für Benutzeranalyse
        "SYMBOLS": {
            "US100": "US100",
            "US30": "US30",
            "SPX500": "SPX500",
            "IWM": "IWM",
            "DAX": "DAX"
        },

        # Technische Analyse-Einstellungen
        "INTERVAL": os.getenv("INTERVAL", "5min"),
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 20)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 50)),

        # Auto-Signal-Einstellungen
        "AUTO_SIGNAL_SYMBOLS": os.getenv("AUTO_SIGNAL_SYMBOLS", "US100,US30,SPX500,IWM,DAX").split(","),
        "AUTO_SIGNAL_INTERVAL": int(os.getenv("AUTO_SIGNAL_INTERVAL", 60)),
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 10))
    }
