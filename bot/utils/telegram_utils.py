# bot/utils/telegram_utils.py

"""
Handles direct interactions with the Telegram API.
Mainly used for update polling and diagnostics.
"""

import requests
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def get_updates_from_telegram(bot_token: str) -> dict:
    """
    Fetches updates from the Telegram Bot API.

    Args:
        bot_token (str): Telegram Bot Token.

    Returns:
        dict: Parsed JSON response if successful, None otherwise.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        logger.debug(f"Telegram API Response Code: {response.status_code}")

        if response.status_code == 200:
            logger.info("Successfully fetched updates from Telegram API.")
            return response.json()
        else:
            logger.error(f"Telegram API error: HTTP {response.status_code} – {response.text}")
            return None

    except requests.exceptions.Timeout:
        logger.warning("Telegram API request timed out after 10 seconds.")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Telegram API general request error: {e}")
        return None

    except Exception as e:
        logger.critical(f"Unexpected fatal error during Telegram API update fetch: {e}")
        return None
