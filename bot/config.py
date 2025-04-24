import os
from dotenv import load_dotenv

load_dotenv()  # Lädt alle Umgebungsvariablen

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "")
TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Analyseparameter – feinjustiert für Hochfrequenz-Scans
INTERVAL = os.getenv("INTERVAL", "1")  # Minutenintervall: 1 = 1m
RSI_PERIOD = int(os.getenv("RSI_PERIOD", "14"))
EMA_SHORT_PERIOD = int(os.getenv("EMA_SHORT_PERIOD", "9"))
EMA_LONG_PERIOD = int(os.getenv("EMA_LONG_PERIOD", "21"))

# Signal-Konfiguration für maximalen Output
SIGNAL_CHECK_INTERVAL = int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", "60"))  # Wie oft gescannt wird (Sek.)
MAX_SIGNALS_PER_HOUR = int(os.getenv("MAX_SIGNALS_PER_HOUR", "9000"))  # Maximal mögliche Signale pro Stunde

# Fokus auf 7 US-Märkte mit hoher Volatilität & Liquidität
AUTO_SIGNAL_SYMBOLS = os.getenv("AUTO_SIGNAL_SYMBOLS", "US100,US30,SPX500,IWM,QQQ,DIA,MDY").split(",")
