import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    """Perfekte, stabile Live-Einstellungen."""
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("DANIEL_TELEGRAM_ID"),
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY"),
        "SYMBOLS": {
            "QQQ": "QQQ",  # Nasdaq-100 ETF
            "SPY": "SPY",  # S&P 500 ETF
            "DIA": "DIA",  # Dow Jones ETF
            "IWM": "IWM",  # Russell 2000 ETF
            "MDY": "MDY",  # S&P MidCap 400 ETF
        },
        "INTERVAL": os.getenv("INTERVAL", "5min"),
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 20)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 50)),
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 300)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 10))
    }