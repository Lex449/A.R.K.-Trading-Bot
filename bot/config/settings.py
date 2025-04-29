# bot/config/settings.py

"""
A.R.K. Settings Loader – Ultra Diamond Build
Lädt und validiert alle Umgebungsvariablen aus der .env Datei für maximale Stabilität.
"""

import os
import logging
from dotenv import load_dotenv
from bot.utils.logger import setup_logger

# === Load Environment Variables Early ===
load_dotenv()

# === Setup Logger Early ===
logger = setup_logger(__name__)

def get_settings() -> dict:
    """
    Loads and validates all environment variables for the bot.
    """

    # --- Core API Tokens ---
    bot_token = os.getenv("BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    finnhub_api_key = os.getenv("FINNHUB_API_KEY")

    if not bot_token:
        logger.critical("❌ [Settings] Missing BOT_TOKEN in .env.")
        raise ValueError("BOT_TOKEN is required.")
    if not telegram_chat_id:
        logger.critical("❌ [Settings] Missing TELEGRAM_CHAT_ID in .env.")
        raise ValueError("TELEGRAM_CHAT_ID is required.")
    if not finnhub_api_key:
        logger.critical("❌ [Settings] Missing FINNHUB_API_KEY in .env.")
        raise ValueError("FINNHUB_API_KEY is required.")

    # --- Trading Settings ---
    interval = os.getenv("INTERVAL", "1min")
    auto_signal_symbols = os.getenv("AUTO_SIGNAL_SYMBOLS", "")
    symbols_list = [s.strip().upper() for s in auto_signal_symbols.split(",") if s.strip()]

    # --- Bot Behavior ---
    environment = os.getenv("ENVIRONMENT", "Production").capitalize()
    bot_language = os.getenv("BOT_LANGUAGE", "en").lower()

    # --- Signal Settings ---
    signal_check_interval_sec = int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60))
    max_signals_per_hour = int(os.getenv("MAX_SIGNALS_PER_HOUR", 150))

    # --- Advanced Modules ---
    news_filter_enabled = os.getenv("NEWS_FILTER_ENABLED", "True").lower() == "true"
    backup_news_enabled = os.getenv("BACKUP_NEWS_ENABLED", "True").lower() == "true"
    confidence_adjustment_enabled = os.getenv("CONFIDENCE_ADJUSTMENT_ENABLED", "False").lower() == "true"
    confidence_scaling_factor = float(os.getenv("CONFIDENCE_SCALING_FACTOR", 1.0))

    # --- Watchdog System ---
    watchdog_enabled = os.getenv("WATCHDOG_ENABLED", "True").lower() == "true"
    watchdog_interval_min = int(os.getenv("WATCHDOG_INTERVAL_MIN", 30))

    logger.info(f"✅ [Settings] Loaded successfully. Environment: {environment}")

    return {
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,
        "FINNHUB_API_KEY": finnhub_api_key,
        "INTERVAL": interval,
        "AUTO_SIGNAL_SYMBOLS": symbols_list,
        "ENVIRONMENT": environment,
        "BOT_LANGUAGE": bot_language,
        "SIGNAL_CHECK_INTERVAL_SEC": signal_check_interval_sec,
        "MAX_SIGNALS_PER_HOUR": max_signals_per_hour,
        "NEWS_FILTER_ENABLED": news_filter_enabled,
        "BACKUP_NEWS_ENABLED": backup_news_enabled,
        "CONFIDENCE_ADJUSTMENT_ENABLED": confidence_adjustment_enabled,
        "CONFIDENCE_SCALING_FACTOR": confidence_scaling_factor,
        "WATCHDOG_ENABLED": watchdog_enabled,
        "WATCHDOG_INTERVAL_MIN": watchdog_interval_min,
    }
