import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_settings():
    """
    Loads and validates the environment variables required for the bot.
    """

    # === Mandatory Variables ===
    bot_token = os.getenv("BOT_TOKEN")
    if not bot_token:
        raise ValueError("❌ BOT_TOKEN is missing in .env. Please provide a valid Telegram bot token.")

    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not telegram_chat_id:
        raise ValueError("❌ TELEGRAM_CHAT_ID is missing in .env. Please provide a valid Telegram chat ID.")

    finnhub_api_key = os.getenv("FINNHUB_API_KEY")
    if not finnhub_api_key:
        raise ValueError("❌ FINNHUB_API_KEY is missing in .env. Please provide a valid Finnhub API key.")

    # === Optional Variables ===
    interval = os.getenv("INTERVAL", "1min")
    valid_intervals = ["1min", "5min", "15min", "30min", "60min"]
    if interval not in valid_intervals:
        raise ValueError(f"❌ Invalid INTERVAL `{interval}`. Expected one of: {', '.join(valid_intervals)}.")

    # === Assemble Configuration ===
    return {
        # Telegram
        "BOT_TOKEN": bot_token,
        "TELEGRAM_CHAT_ID": telegram_chat_id,

        # Analysis Configuration
        "RSI_PERIOD": int(os.getenv("RSI_PERIOD", 14)),
        "EMA_SHORT_PERIOD": int(os.getenv("EMA_SHORT_PERIOD", 9)),
        "EMA_LONG_PERIOD": int(os.getenv("EMA_LONG_PERIOD", 21)),
        "INTERVAL": interval,

        # Signal Configuration
        "AUTO_SIGNAL_SYMBOLS": [s.strip() for s in os.getenv("AUTO_SIGNAL_SYMBOLS", "").split(",") if s.strip()],
        "SIGNAL_CHECK_INTERVAL_SEC": int(os.getenv("SIGNAL_CHECK_INTERVAL_SEC", 60)),
        "MAX_SIGNALS_PER_HOUR": int(os.getenv("MAX_SIGNALS_PER_HOUR", 150)),

        # Finnhub API
        "FINNHUB_API_KEY": finnhub_api_key
    }
