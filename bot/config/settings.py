import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    return {
        "BOT_TOKEN": os.getenv("BOT_TOKEN"),
        "TELEGRAM_CHAT_ID": os.getenv("TELEGRAM_CHAT_ID"),
        "TWELVEDATA_API_KEY": os.getenv("TWELVEDATA_API_KEY"),

        "SYMBOLS": {
            "QQQ": "QQQ",     # Nasdaq ETF
            "SPY": "SPY",     # S&P500 ETF
            "DIA": "DIA",     # Dow Jones ETF
            "IWM": "IWM",     # Russell 2000
            "MDY": "MDY"      # MidCap 400
        },

        "INTERVAL": os.getenv("INTERVAL", "5min"),
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 20)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 50)),

        "AUTO_SIGNAL_SYMBOLS": os.getenv("AUTO_SIGNAL_SYMBOLS", "QQQ,SPY,DIA,IWM,MDY").split(","),
        "AUTO_SIGNAL_INTERVAL": int(os.getenv("AUTO_SIGNAL_INTERVAL", 60)),
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 10))
    }
