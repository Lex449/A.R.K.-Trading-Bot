import os
from dotenv import load_dotenv

load_dotenv()

def get_settings():
    # === Prüfung der Umgebungsvariablen ===
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("❌ BOT_TOKEN nicht in .env gefunden.")

    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not telegram_chat_id:
        raise ValueError("❌ TELEGRAM_CHAT_ID nicht in .env gefunden.")
    
    twelvedata_api_key = os.getenv("TWELVEDATA_API_KEY")
    if not twelvedata_api_key:
        raise ValueError("❌ TWELVEDATA_API_KEY nicht in .env gefunden.")
    
    # === Überprüfen der Werte ===
    interval = os.getenv("INTERVAL", "1min")
    if interval not in ["1min", "5min", "15min", "30min", "60min"]:
        raise ValueError(f"❌ Ungültiges Intervall `{interval}` in .env. Erwartet: 1min, 5min, 15min, 30min oder 60min.")

    # === Rückgabewerte ===
    return {
        # Telegram Konfiguration
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,

        # Analyse-Konfiguration
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),
        "INTERVAL": interval,

        # Signal-Konfiguration
        "AUTO_SIGNAL_SYMBOLS": [s.strip() for s in os.getenv("AUTO_SIGNAL_SYMBOLS", "").split(",") if s.strip()],
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 150)),

        # TwelveData API Key
        "TWELVEDATA_API_KEY": twelvedata_api_key
    }
