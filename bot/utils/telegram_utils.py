# bot/utils/telegram_utils.py

"""
A.R.K. Telegram Utils – API Interaction Module.
Handles direct interactions with the Telegram API for updates polling and diagnostics.
"""

import requests
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Telegram API Base URL
TELEGRAM_API_BASE = "https://api.telegram.org"

def get_updates_from_telegram(bot_token: str) -> dict | None:
    """
    Fetches updates from the Telegram Bot API.

    Args:
        bot_token (str): Telegram Bot Token.

    Returns:
        dict | None: Parsed JSON response if successful, otherwise None.
    """
    url = f"{TELEGRAM_API_BASE}/bot{bot_token}/getUpdates"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        logger.debug(f"[Telegram API] Response Code: {response.status_code}")

        if response.status_code == 200:
            logger.info("[Telegram API] Successfully fetched updates.")
            return response.json()
        else:
            logger.error(f"[Telegram API] Error: HTTP {response.status_code} – {response.text}")
            return None

    except requests.exceptions.Timeout:
        logger.warning("[Telegram API] Request timed out after 10 seconds.")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"[Telegram API] General request error: {e}")
        return None

    except Exception as e:
        logger.critical(f"[Telegram API] Unexpected fatal error: {e}")
        return None
