# bot/config/settings.py

import os
from dotenv import load_dotenv
import logging

# === Load Environment Variables ===
load_dotenv()

# === Setup Logging ===
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_settings():
    """
    Loads and validates environment variables for A.R.K. Trading Bot.
    """

    # === Mandatory Variables ===
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("❌ BOT_TOKEN is missing in .env.")
        raise ValueError("❌ BOT_TOKEN is missing. Please check your .env file.")

    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not telegram_chat_id:
        logger.error("❌ TELEGRAM_CHAT_ID is missing in .env.")
        raise ValueError("❌ TELEGRAM_CHAT_ID is missing. Please check your .env file.")

    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    if not finnhub_api_key:
        logger.error("❌ FINNHUB_API_KEY is missing in .env.")
        raise ValueError("❌ FINNHUB_API_KEY is missing. Please check your .env file.")

    # === Optional Variables ===
    interval = os.getenv("INTERVAL", "1min")
    if interval not in ["1min", "5min", "15min", "30min", "60min"]:
        logger.warning(f"⚠️ Invalid INTERVAL '{interval}' found. Defaulting to '1min'.")
        interval = "1min"

    auto_signal_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    if not auto_signal_symbols:
        logger.warning("⚠️ No symbols defined in AUTO_SIGNAL_SYMBOLS. Defaulting to empty list.")

    environment = os.getenv("ENVIRONMENT", "Production").capitalize()
    if environment not in ["Production", "Development"]:
        environment = "Production"

    logger.info(f"✅ Settings loaded successfully. Running in '{environment}' mode.")

    # === Assemble Settings ===
    settings = {
        # Telegram
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,

        # Trading Parameters
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),
        "INTERVAL": interval,

        # Auto Signal Settings
        "AUTO_SIGNAL_SYMBOLS": [s.strip().upper() for s in auto_signal_symbols.split(",") if s.strip()],
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 150)),

        # API Keys
        "FINNHUB_API_KEY": finnhub_api_key,

        # Environment Info
        "ENVIRONMENT": environment
    }

    return settings
