"""
A.R.K. Settings Loader – Ultra Diamond Build 2025.4  
Lädt und validiert alle Umgebungsvariablen aus der .env Datei für maximale Stabilität.  
Inklusive Auto-Split für AUTO_SIGNAL_SYMBOLS als Liste.  
Made in Bali. Engineered with German Precision.
"""

import os
from dotenv import load_dotenv
from bot.utils.logger import setup_logger

# Load .env early
load_dotenv()

# Setup structured logger
logger = setup_logger(__name__)

def get_settings() -> dict:
    """
    Lädt, validiert und strukturiert alle relevanten ENV-Variablen.
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
            logger.warning(f"⚠️ [Settings] Failed to cast {key}. Using raw string value.")
            return value

    # === Core Tokens ===
    bot_token = get_env_var("BOT_TOKEN", required=True)
    telegram_chat_id = get_env_var("TELEGRAM_CHAT_ID", required=True)
    finnhub_api_key = get_env_var("FINNHUB_API_KEY", required=True)

    # === Trading Setup ===
    interval = get_env_var("INTERVAL", default="1min")
    raw_symbols = get_env_var("AUTO_SIGNAL_SYMBOLS", default="")
    auto_signal_symbols = (
        raw_symbols if isinstance(raw_symbols, list)
        else [s.strip().upper() for s in raw_symbols.split(",") if s.strip()]
    )

    # === General Bot Behavior ===
    environment = get_env_var("ENVIRONMENT", default="Production").capitalize()
    bot_language = get_env_var("BOT_LANGUAGE", default="en").lower()

    # === Signal Module ===
    signal_check_interval_sec = get_env_var("SIGNAL_CHECK_INTERVAL_SEC", default=60, cast_type=int)
    max_signals_per_hour = get_env_var("MAX_SIGNALS_PER_HOUR", default=150, cast_type=int)

    # === AI Confidence Scaling ===
    confidence_adjustment_enabled = get_env_var("CONFIDENCE_ADJUSTMENT_ENABLED", default="False").lower() == "true"
    confidence_scaling_factor = get_env_var("CONFIDENCE_SCALING_FACTOR", default=1.0, cast_type=float)

    # === News Module ===
    news_filter_enabled = get_env_var("NEWS_FILTER_ENABLED", default="True").lower() == "true"
    backup_news_enabled = get_env_var("BACKUP_NEWS_ENABLED", default="True").lower() == "true"

    # === Watchdog Module ===
    watchdog_enabled = get_env_var("WATCHDOG_ENABLED", default="True").lower() == "true"
    watchdog_interval_min = get_env_var("WATCHDOG_INTERVAL_MIN", default=30, cast_type=int)

    # === Market Time Control ===
    us_market_open_hour = get_env_var("US_MARKET_OPEN_HOUR", default=13, cast_type=int)   # UTC → 13:30 NYSE
    us_market_close_hour = get_env_var("US_MARKET_CLOSE_HOUR", default=20, cast_type=int) # UTC → 20:00 NYSE

    logger.info(f"✅ [Settings] Loaded successfully. Environment: {environment} | Language: {bot_language}")

    return {
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,
        "FINNHUB_API_KEY": finnhub_api_key,
        "INTERVAL": interval,
        "AUTO_SIGNAL_SYMBOLS": auto_signal_symbols,
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
        "US_MARKET_CLOSE_HOUR": us_market_close_hour
    }
