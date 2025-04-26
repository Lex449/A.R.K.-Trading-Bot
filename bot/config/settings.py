# bot/config/settings.py

import os
import logging
from dotenv import load_dotenv
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Load Environment Variables ===
load_dotenv()

def get_settings() -> dict:
    """
    Loads and validates environment variables for the bot's configuration.
    Provides robust error handling and safe defaults.
    """

    # === Mandatory Variables ===
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        logger.critical("❌ BOT_TOKEN missing in .env. Cannot start the bot.")
        raise ValueError("❌ BOT_TOKEN is missing. Please add it to your .env file.")

    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not telegram_chat_id:
        logger.critical("❌ TELEGRAM_CHAT_ID missing in .env. Cannot start the bot.")
        raise ValueError("❌ TELEGRAM_CHAT_ID is missing. Please add it to your .env file.")

    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    if not finnhub_api_key:
        logger.critical("❌ FINNHUB_API_KEY missing in .env. Cannot fetch market data.")
        raise ValueError("❌ FINNHUB_API_KEY is missing. Please add it to your .env file.")

    # === Optional Trading Parameters ===
    interval = os.getenv("INTERVAL", "1min")
    allowed_intervals = ["1min", "5min", "15min", "30min", "60min"]
    if interval not in allowed_intervals:
        logger.warning(f"⚠️ Invalid INTERVAL '{interval}' found. Defaulting to '1min'.")
        interval = "1min"

    auto_signal_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    symbols = [s.strip().upper() for s in auto_signal_symbols.split(",") if s.strip()]

    if not symbols:
        logger.warning("⚠️ No AUTO_SIGNAL_SYMBOLS defined. Auto analysis will be inactive.")

    # === Final Assembled Settings ===
    settings = {
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,
        "FINNHUB_API_KEY": finnhub_api_key,

        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),
        "INTERVAL": interval,

        "AUTO_SIGNAL_SYMBOLS": symbols,
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 150)),
    }

    logger.info("✅ Settings loaded successfully.")
    return settings
