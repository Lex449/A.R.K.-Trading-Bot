import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
TWELVEDATA_API_KEY = os.getenv("TWELVEDATA_API_KEY")

SYMBOLS = {
    "QQQ": "QQQ",  # Nasdaq-100 ETF
    "SPY": "SPY",  # S&P 500 ETF
    "DIA": "DIA",  # Dow Jones ETF
    "IWM": "IWM",  # Russell 2000 ETF
    "MDY": "MDY",  # S&P MidCap 400 ETF
}

INTERVAL = "5min"
RSI_PERIOD = 14
EMA_SHORT_PERIOD = 20
EMA_LONG_PERIOD = 50

SIGNAL_CHECK_INTERVAL_SEC = 300
MAX_SIGNALS_PER_HOUR = 10