# bot/utils/telegram_utils.py

"""
A.R.K. Telegram Utilities – Ultra Premium API Interaction Layer.
Handles secure fetching of updates and diagnostics from the Telegram Bot API.
Built for Maximum Stability, Logging Intelligence & Future API Expansion.

Made in Bali. Engineered with German Precision.
"""

import requests
from typing import Optional
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Telegram API base endpoint
TELEGRAM_API_BASE = "https://api.telegram.org"

# === GET UPDATES ===
def get_updates_from_telegram(bot_token: str, timeout: int = 8) -> Optional[dict]:
    """
    Securely fetches updates from the Telegram Bot API.

    Args:
        bot_token (str): Telegram bot token from BotFather.
        timeout (int): Timeout for the request in seconds.

    Returns:
        dict | None: Parsed response or None on failure.
    """

    url = f"{TELEGRAM_API_BASE}/bot{bot_token}/getUpdates"
    headers = {"Accept": "application/json"}

    try:
        logger.debug(f"[TelegramAPI] Requesting updates from: {url}")
        response = requests.get(url, headers=headers, timeout=timeout)

        if not response.ok:
            logger.warning(
                f"⚠️ [TelegramAPI] HTTP {response.status_code} – {response.text}"
            )
            return None

        json_data = response.json()

        if not json_data.get("ok", False):
            logger.warning(f"⚠️ [TelegramAPI] API returned ok=False → {json_data}")
            return None

        logger.info("✅ [TelegramAPI] Updates successfully received.")
        return json_data

    except requests.exceptions.Timeout:
        logger.error(f"⏳ [TelegramAPI] Timeout after {timeout} seconds.")
    except requests.exceptions.ConnectionError as e:
        logger.error(f"🔌 [TelegramAPI] Connection Error: {e}")
    except requests.exceptions.RequestException as e:
        logger.error(f"🚨 [TelegramAPI] Request Exception: {e}")
    except Exception as e:
        logger.critical(f"🔥 [TelegramAPI] Unexpected Fatal Error: {e}")

    return None
