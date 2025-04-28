"""
A.R.K. Trading Bot – Ultra Diamond Settings Loader
Fault-Tolerant, API-Optimized, Fully Scalable.
"""

import os
import logging
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Setup Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_settings() -> dict:
    """
    Loads, validates, and optimizes all environment settings for A.R.K. Bot.
    """

    # === Critical Essentials ===
    bot_token = os.getenv("BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")

    if not bot_token:
        logger.critical("❌ BOT_TOKEN is missing. Check your .env file.")
        raise ValueError("❌ BOT_TOKEN missing. Please fix .env file.")
    if not telegram_chat_id:
        logger.critical("❌ TELEGRAM_CHAT_ID is missing. Check your .env file.")
        raise ValueError("❌ TELEGRAM_CHAT_ID missing. Please fix .env file.")
    if not finnhub_api_key:
        logger.critical("❌ FINNHUB_API_KEY is missing. Check your .env file.")
        raise ValueError("❌ FINNHUB_API_KEY missing. Please fix .env file.")

    # === Trading Parameters ===
    interval = os.getenv("INTERVAL", "1min")
    if interval not in ["1min", "5min", "15min", "30min", "60min"]:
        logger.warning(f"⚠️ Invalid INTERVAL '{interval}'. Defaulting to '1min'.")
        interval = "1min"

    auto_signal_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    symbols_list = [s.strip().upper() for s in auto_signal_symbols.split(",") if s.strip()]
    if not symbols_list:
        logger.warning("⚠️ No AUTO_SIGNAL_SYMBOLS defined. Default: Empty list.")

    # === Bot Behavior ===
    environment = os.getenv("ENVIRONMENT", "Production").capitalize()
    if environment not in ["Production", "Development"]:
        logger.warning(f"⚠️ Invalid ENVIRONMENT '{environment}'. Defaulting to 'Production'.")
        environment = "Production"

    bot_language = os.getenv("BOT_LANGUAGE", "en").lower()
    if bot_language not in ["en", "de"]:
        logger.warning(f"⚠️ Invalid BOT_LANGUAGE '{bot_language}'. Defaulting to 'en'.")
        bot_language = "en"

    # === News Module Control ===
    news_filter_enabled = os.getenv("NEWS_FILTER_ENABLED", "True").lower() == "true"
    backup_news_enabled = os.getenv("BACKUP_NEWS_ENABLED", "True").lower() == "true"

    # === Signal Control ===
    signal_check_interval_sec = int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60))
    max_signals_per_hour = int(os.getenv("MAX_SIGNALS_PER_HOUR", 150))

    # === Deep Learning Confidence Control ===
    confidence_adjustment_enabled = os.getenv("CONFIDENCE_ADJUSTMENT_ENABLED", "False").lower() == "true"
    confidence_scaling_factor = float(os.getenv("CONFIDENCE_SCALING_FACTOR", 1.0))

    logger.info(f"✅ Settings loaded successfully. Environment: {environment}")

    return {
        # Telegram
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,

        # API
        "FINNHUB_API_KEY": finnhub_api_key,

        # Trading Settings
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),
        "INTERVAL": interval,

        # Auto Signal Settings
        "AUTO_SIGNAL_SYMBOLS": symbols_list,
        "SIGNAL_CHECK_INTERVAL_SEC": signal_check_interval_sec,
        "MAX_SIGNALS_PER_HOUR": max_signals_per_hour,

        # News Handling
        "NEWS_FILTER_ENABLED": news_filter_enabled,
        "BACKUP_NEWS_ENABLED": backup_news_enabled,

        # Environment
        "ENVIRONMENT": environment,
        "BOT_LANGUAGE": bot_language,

        # Deep Learning Confidence
        "CONFIDENCE_ADJUSTMENT_ENABLED": confidence_adjustment_enabled,
        "CONFIDENCE_SCALING_FACTOR": confidence_scaling_factor,
    }
