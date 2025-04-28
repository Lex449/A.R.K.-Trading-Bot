# bot/config/settings.py

"""
A.R.K. Trading Bot – Settings Loader (ULTRA Masterclass Build)
Supercharged für Skalierung, Fehlerprävention und dynamisches Handling.
"""

import os
import logging
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv()

# === Setup Logger ===
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_settings():
    """
    Lädt und validiert ALLE .env-Variablen für den stabilen Betrieb des A.R.K. Trading Bots.
    """

    # === Telegram Essentials ===
    bot_token = os.getenv("BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token:
        logger.error("❌ BOT_TOKEN fehlt in der .env Datei.")
        raise ValueError("❌ BOT_TOKEN fehlt. Bitte .env überprüfen.")
    if not telegram_chat_id:
        logger.error("❌ TELEGRAM_CHAT_ID fehlt in der .env Datei.")
        raise ValueError("❌ TELEGRAM_CHAT_ID fehlt. Bitte .env überprüfen.")

    # === API Keys ===
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    if not finnhub_api_key:
        logger.error("❌ FINNHUB_API_KEY fehlt in der .env Datei.")
        raise ValueError("❌ FINNHUB_API_KEY fehlt. Bitte .env überprüfen.")

    # === Trading Settings ===
    interval = os.getenv("INTERVAL", "5min").lower()
    valid_intervals = ["1min", "5min", "15min", "30min", "60min"]
    if interval not in valid_intervals:
        logger.warning(f"⚠️ Ungültiges INTERVAL '{interval}' erkannt. Setze auf '5min'.")
        interval = "5min"

    auto_signal_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    symbols_list = [s.strip().upper() for s in auto_signal_symbols.split(",") if s.strip()]
    if not symbols_list:
        logger.warning("⚠️ Keine AUTO_SIGNAL_SYMBOLS definiert. Standard: Leere Liste.")

    # === News Handling ===
    news_filter_enabled = os.getenv("NEWS_FILTER_ENABLED", "True").lower() == "true"
    backup_news_enabled = os.getenv("BACKUP_NEWS_ENABLED", "True").lower() == "true"

    # === Bot Language ===
    bot_language = os.getenv("BOT_LANGUAGE", "en").lower()
    if bot_language not in ["en", "de"]:
        bot_language = "en"

    # === Environment Type ===
    environment = os.getenv("ENVIRONMENT", "Production").capitalize()
    if environment not in ["Production", "Development"]:
        logger.warning(f"⚠️ Ungültiges ENVIRONMENT '{environment}' erkannt. Setze auf 'Production'.")
        environment = "Production"

    # === Signal Controls ===
    signal_check_interval_sec = int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60))
    max_signals_per_hour = int(os.getenv("MAX_SIGNALS_PER_HOUR", 150))
    signal_confidence_threshold = int(os.getenv("SIGNAL_CONFIDENCE_THRESHOLD", 55))
    move_alert_threshold = float(os.getenv("MOVE_ALERT_THRESHOLD", 2.0))

    logger.info(f"✅ Settings erfolgreich geladen für Environment: {environment}")

    # === Final Settings Paket ===
    settings = {
        # Telegram
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,

        # API
        "FINNHUB_API_KEY": finnhub_api_key,

        # Trading
        "INTERVAL": interval,
        "AUTO_SIGNAL_SYMBOLS": symbols_list,
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),

        # Signal Control
        "SIGNAL_CHECK_INTERVAL_SEC": signal_check_interval_sec,
        "MAX_SIGNALS_PER_HOUR": max_signals_per_hour,
        "SIGNAL_CONFIDENCE_THRESHOLD": signal_confidence_threshold,
        "MOVE_ALERT_THRESHOLD": move_alert_threshold,

        # News
        "NEWS_FILTER_ENABLED": news_filter_enabled,
        "BACKUP_NEWS_ENABLED": backup_news_enabled,

        # Bot Setup
        "BOT_LANGUAGE": bot_language,
        "ENVIRONMENT": environment,
    }

    return settings
