# bot/utils/telegram_utils.py

import logging
import requests

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_updates_from_telegram(bot_token: str) -> dict:
    """
    Fetches the latest updates from the Telegram API.
    
    Args:
        bot_token (str): Telegram bot token.

    Returns:
        dict: Parsed response if successful, otherwise None.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
    headers = {"Accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, timeout=10)

        logger.debug(f"[Telegram API] Status: {response.status_code}")
        if response.status_code == 200:
            logger.info("[Telegram API] Successfully retrieved updates.")
            return response.json()
        else:
            logger.error(f"[Telegram API] Failed: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.Timeout:
        logger.warning("[Telegram API] Request timed out.")
        return None

    except requests.exceptions.RequestException as e:
        logger.error(f"[Telegram API] Request error: {str(e)}")
        return None

    except Exception as e:
        logger.critical(f"[Telegram API] Unexpected error: {str(e)}")
        return None
