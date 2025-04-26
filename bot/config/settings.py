# bot/config/settings.py

import os
from dotenv import load_dotenv
import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Load environment variables
load_dotenv()

def get_settings():
    """
    Loads and validates the environment variables required for the bot.
    """

    # === Load Mandatory Variables ===
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.error("❌ BOT_TOKEN missing in .env.")
        raise ValueError("❌ BOT_TOKEN missing in .env. Please set it.")

    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not telegram_chat_id:
        logger.error("❌ TELEGRAM_CHAT_ID missing in .env.")
        raise ValueError("❌ TELEGRAM_CHAT_ID missing in .env. Please set it.")

    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    if not finnhub_api_key:
        logger.error("❌ FINNHUB_API_KEY missing in .env.")
        raise ValueError("❌ FINNHUB_API_KEY missing in .env. Please set it.")

    # === Load Optional Variables ===
    interval = os.getenv("INTERVAL", "1min")
    valid_intervals = ["1min", "5min", "15min", "30min", "60min"]
    if interval not in valid_intervals:
        logger.warning(f"⚠️ Invalid INTERVAL '{interval}' set. Falling back to '1min'.")
        interval = "1min"

    # === Load Signal Symbols ===
    auto_signal_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    if not auto_signal_symbols:
        logger.warning("⚠️ AUTO_SIGNAL_SYMBOLS is empty. No symbols to monitor.")

    # === Final Assembly ===
    settings = {
        # Telegram
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,

        # Analysis Settings
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),
        "INTERVAL": interval,

        # Signal Settings
        "AUTO_SIGNAL_SYMBOLS": [s.strip() for s in auto_signal_symbols.split(",") if s.strip()],
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 150)),

        # APIs
        "FINNHUB_API_KEY": finnhub_api_key
    }

    logger.info("✅ Settings successfully loaded.")
    return settings
