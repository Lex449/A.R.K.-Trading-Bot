"""
A.R.K. Settings Loader – Ultra Diamond Build 3.0
Lädt und validiert alle Umgebungsvariablen aus der .env Datei für maximale Stabilität.
"""

import os
from dotenv import load_dotenv
from bot.utils.logger import setup_logger

# === Load .env Early ===
load_dotenv()

# === Setup Logger ===
logger = setup_logger(__name__)

def get_settings() -> dict:
    """
    Loads, validates, and structures all environment settings.
    """

    def get_env_var(key: str, required: bool = False, default=None, cast_type=None):
        value = os.getenv(key)
        if value is None:
            if required:
                logger.critical(f"❌ [Settings] Missing required environment variable: {key}")
                raise ValueError(f"{key} is required.")
            return default
        try:
            return cast_type(value) if cast_type else value
        except Exception:
            logger.warning(f"⚠️ [Settings] Could not cast {key}. Using raw value.")
            return value

    # === Core API Tokens ===
    bot_token = get_env_var("BOT_TOKEN", required=True)
    telegram_chat_id = get_env_var("TELEGRAM_CHAT_ID", required=True)
    finnhub_api_key = get_env_var("FINNHUB_API_KEY", required=True)

    # === Trading Settings ===
    interval = get_env_var("INTERVAL", default="1min")
    auto_signal_symbols = get_env_var("AUTO_SIGNAL_SYMBOLS", default="")
    symbols_list = [s.strip().upper() for s in auto_signal_symbols.split(",") if s.strip()]

    # === Bot Behavior ===
    environment = get_env_var("ENVIRONMENT", default="Production").capitalize()
    bot_language = get_env_var("BOT_LANGUAGE", default="en").lower()

    # === Signal Settings ===
    signal_check_interval_sec = get_env_var("SIGNAL_CHECK_INTERVAL_SEC", default=60, cast_type=int)
    max_signals_per_hour = get_env_var("MAX_SIGNALS_PER_HOUR", default=150, cast_type=int)

    # === Advanced Modules ===
    news_filter_enabled = get_env_var("NEWS_FILTER_ENABLED", default="True").lower() == "true"
    backup_news_enabled = get_env_var("BACKUP_NEWS_ENABLED", default="True").lower() == "true"
    confidence_adjustment_enabled = get_env_var("CONFIDENCE_ADJUSTMENT_ENABLED", default="False").lower() == "true"
    confidence_scaling_factor = get_env_var("CONFIDENCE_SCALING_FACTOR", default=1.0, cast_type=float)

    # === Watchdog System ===
    watchdog_enabled = get_env_var("WATCHDOG_ENABLED", default="True").lower() == "true"
    watchdog_interval_min = get_env_var("WATCHDOG_INTERVAL_MIN", default=30, cast_type=int)

    # === US Market Sessions ===
    us_market_open_hour = get_env_var("US_MARKET_OPEN_HOUR", default=13, cast_type=int)  # UTC 13:30
    us_market_close_hour = get_env_var("US_MARKET_CLOSE_HOUR", default=20, cast_type=int)  # UTC 20:00

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
        "US_MARKET_OPEN_HOUR": us_market_open_hour,
        "US_MARKET_CLOSE_HOUR": us_market_close_hour,
    }
