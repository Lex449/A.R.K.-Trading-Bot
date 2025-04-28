"""
A.R.K. Telegram Utilities – Ultra Premium API Interaction Layer.
Handles secure fetching of updates and diagnostics from the Telegram Bot API.
Built for Maximum Stability and Future API Expansion.
"""

import requests
from bot.utils.logger import setup_logger

# Setup Structured Logger
logger = setup_logger(__name__)

# Telegram API Base URL
TELEGRAM_API_BASE = "https://api.telegram.org"

def get_updates_from_telegram(bot_token: str) -> dict | None:
    """
    Fetches latest updates from the Telegram Bot API.

    Args:
        bot_token (str): The Bot Token provided by BotFather.

    Returns:
        dict | None: JSON payload if successful, None otherwise.
    """
    url = f"{TELEGRAM_API_BASE}/bot{bot_token}/getUpdates"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=8)

        if response.ok:
            logger.info(f"✅ [Telegram API] Updates fetched successfully.")
            return response.json()
        else:
            logger.warning(
                f"⚠️ [Telegram API] Non-200 response: {response.status_code} – {response.text}"
            )
            return None

    except requests.exceptions.Timeout:
        logger.error("⏳ [Telegram API] Timeout after 8 seconds.")
        return None

    except requests.exceptions.ConnectionError as e:
        logger.error(f"🔌 [Telegram API] Connection error: {e}")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"🚨 [Telegram API] Request error: {e}")
        return None

    except Exception as e:
        logger.critical(f"🔥 [Telegram API] Unexpected Fatal Error: {e}")
        return None
