"""
A.R.K. Trading Bot – Ultra Diamond Settings Loader v2.1
Maximal Stabilität, Fehler-Toleranz und Zukunftssicherheit.
"""

import os
import logging
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv()

# === Setup Logger Early ===
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_settings() -> dict:
    """
    Loads and validates all environment variables for the bot.
    """

    # --- Core API Tokens ---
    bot_token = os.getenv("BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")

    if not bot_token:
        logger.critical("❌ Missing BOT_TOKEN in .env file.")
        raise ValueError("❌ BOT_TOKEN is required.")
    if not telegram_chat_id:
        logger.critical("❌ Missing TELEGRAM_CHAT_ID in .env file.")
        raise ValueError("❌ TELEGRAM_CHAT_ID is required.")
    if not finnhub_api_key:
        logger.critical("❌ Missing FINNHUB_API_KEY in .env file.")
        raise ValueError("❌ FINNHUB_API_KEY is required.")

    # --- Trading Settings ---
    interval = os.getenv("INTERVAL", "1min")
    auto_signal_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    symbols_list = [s.strip().upper() for s in auto_signal_symbols.split(",") if s.strip()]

    # --- Bot Behavior ---
    environment = os.getenv("ENVIRONMENT", "Production").capitalize()
    bot_language = os.getenv("BOT_LANGUAGE", "en").lower()

    # --- Signal Control ---
    signal_check_interval_sec = int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60))
    max_signals_per_hour = int(os.getenv("MAX_SIGNALS_PER_HOUR", 150))

    # --- Advanced Modules ---
    news_filter_enabled = os.getenv("NEWS_FILTER_ENABLED", "True").lower() == "true"
    backup_news_enabled = os.getenv("BACKUP_NEWS_ENABLED", "True").lower() == "true"
    confidence_adjustment_enabled = os.getenv("CONFIDENCE_ADJUSTMENT_ENABLED", "False").lower() == "true"
    confidence_scaling_factor = float(os.getenv("CONFIDENCE_SCALING_FACTOR", 1.0))

    # --- Watchdog Settings (reserved for future upgrades) ---
    watchdog_enabled = os.getenv("WATCHDOG_ENABLED", "True").lower() == "true"
    watchdog_interval_min = int(os.getenv("WATCHDOG_INTERVAL_MIN", 30))

    logger.info(f"✅ [Settings] Loaded successfully. Environment: {environment}")

    return {
        # Telegram
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,

        # API Keys
        "FINNHUB_API_KEY": finnhub_api_key,

        # Trading Parameters
        "INTERVAL": interval,
        "AUTO_SIGNAL_SYMBOLS": symbols_list,

        # Bot Control
        "ENVIRONMENT": environment,
        "BOT_LANGUAGE": bot_language,

        # Signal Engine
        "SIGNAL_CHECK_INTERVAL_SEC": signal_check_interval_sec,
        "MAX_SIGNALS_PER_HOUR": max_signals_per_hour,

        # News Engine
        "NEWS_FILTER_ENABLED": news_filter_enabled,
        "BACKUP_NEWS_ENABLED": backup_news_enabled,

        # Confidence Engine
        "CONFIDENCE_ADJUSTMENT_ENABLED": confidence_adjustment_enabled,
        "CONFIDENCE_SCALING_FACTOR": confidence_scaling_factor,

        # Watchdog
        "WATCHDOG_ENABLED": watchdog_enabled,
        "WATCHDOG_INTERVAL_MIN": watchdog_interval_min,
    }
