import os
from dotenv import load_dotenv
load_dotenv()  # lädt Variablen aus .env

FINNHUB_API_KEY     = os.getenv("FINNHUB_API_KEY", "")
TELEGRAM_BOT_TOKEN  = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID    = os.getenv("TELEGRAM_CHAT_ID", "")
INTERVAL            = os.getenv("INTERVAL", "1h")  # Kerzenintervall, z.B. 1h, 1d
RSI_PERIOD          = int(os.getenv("RSI_PERIOD", "14"))
EMA_SHORT_PERIOD    = int(os.getenv("EMA_SHORT_PERIOD", "12"))
EMA_LONG_PERIOD     = int(os.getenv("EMA_LONG_PERIOD", "26"))
SIGNAL_CHECK_INTERVAL = int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", "60"))
MAX_SIGNALS_PER_HOUR  = int(os.getenv("MAX_SIGNALS_PER_HOUR", "3"))
AUTO_SIGNAL_SYMBOLS = os.getenv("AUTO_SIGNAL_SYMBOLS", "US100,US30,DE40,JP225,HK50,SPX500").split(",")
