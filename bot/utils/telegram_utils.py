import logging
import requests

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def get_updates_from_telegram(bot_token: str) -> dict:
    """
    Fetches updates from the Telegram API for the given bot token.

    Args:
        bot_token (str): The Telegram bot token.

    Returns:
        dict: Parsed JSON updates if successful, otherwise None.
    """
    url = f"https://api.telegram.org/bot{bot_token}/getUpdates"

    try:
        response = requests.get(url, timeout=10)

        logger.debug(f"Telegram API Response Code: {response.status_code}")
        logger.debug(f"Telegram API Response Body: {response.text}")

        if response.status_code == 200:
            updates = response.json()
            logger.info("Successfully fetched updates from Telegram.")
            return updates
        else:
            logger.error(f"Error fetching updates: HTTP {response.status_code} - {response.text}")
            return None

    except requests.exceptions.Timeout:
        logger.warning("Request to Telegram API timed out.")
        return None

    except Exception as e:
        logger.error(f"Exception occurred while fetching updates: {str(e)}")
        return None
