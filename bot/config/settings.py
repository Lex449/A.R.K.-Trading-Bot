"""
A.R.K. Trading Bot – Settings Loader
Ultra-Masterclass Build: Präzise. Sicher. Sauber.
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
    Lädt und validiert alle .env-Variablen für den Betrieb des A.R.K. Bots.
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

    # === API Access ===
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    if not finnhub_api_key:
        logger.error("❌ FINNHUB_API_KEY fehlt in der .env Datei.")
        raise ValueError("❌ FINNHUB_API_KEY fehlt. Bitte .env überprüfen.")

    # === Trading Settings ===
    interval = os.getenv("INTERVAL", "1min")
    if interval not in ["1min", "5min", "15min", "30min", "60min"]:
        logger.warning(f"⚠️ Ungültiges INTERVAL '{interval}' erkannt. Setze auf '1min'.")
        interval = "1min"

    auto_signal_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    symbols_list = [s.strip().upper() for s in auto_signal_symbols.split(",") if s.strip()]
    if not symbols_list:
        logger.warning("⚠️ Keine AUTO_SIGNAL_SYMBOLS definiert. Standard: Leere Liste.")

    # === Environment ===
    environment = os.getenv("ENVIRONMENT", "Production").capitalize()
    if environment not in ["Production", "Development"]:
        logger.warning(f"⚠️ Ungültige ENVIRONMENT '{environment}' erkannt. Setze auf 'Production'.")
        environment = "Production"

    logger.info(f"✅ Settings erfolgreich geladen. Environment: {environment}")

    # === Final Settings Paket ===
    settings = {
        # Telegram
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,

        # Trading
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),
        "INTERVAL": interval,

        # Auto Signal
        "AUTO_SIGNAL_SYMBOLS": symbols_list,
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 150)),

        # API
        "FINNHUB_API_KEY": finnhub_api_key,

        # Deployment Info
        "ENVIRONMENT": environment,
    }

    return settings
