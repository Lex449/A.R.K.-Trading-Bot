"""
A.R.K. User Timezone Manager – Final Global Build.
Handles user-specific timezones with full validation, logging, and persistence.
Made in Bali. Engineered with German Precision.
"""

import json
import os
from typing import Dict, List
from pytz import all_timezones
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Constants
USER_TIMEZONE_FILE = "user_timezones.json"
DEFAULT_TIMEZONE = "UTC"

# === Load on demand (not cached globally for write accuracy) ===

def load_user_timezones() -> Dict[str, str]:
    """
    Loads user timezone mappings from disk.

    Returns:
        Dict[str, str]: Mapping of chat_id (as str) → timezone string
    """
    if os.path.exists(USER_TIMEZONE_FILE):
        try:
            with open(USER_TIMEZONE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info("✅ [TimezoneManager] User timezones loaded.")
                return data
        except Exception as e:
            logger.warning(f"⚠️ [TimezoneManager] Failed to load file: {e}")
    return {}

def save_user_timezones(data: Dict[str, str]) -> None:
    """
    Saves timezone data to disk.

    Args:
        data (Dict[str, str]): Mapping of chat_id to timezone.
    """
    try:
        with open(USER_TIMEZONE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        logger.info("✅ [TimezoneManager] User timezones saved.")
    except Exception as e:
        logger.error(f"❌ [TimezoneManager] Failed to save timezones: {e}")

def get_user_timezone(chat_id: int) -> str:
    """
    Gets the timezone for a user, or fallback to UTC.

    Args:
        chat_id (int): Telegram Chat ID.

    Returns:
        str: Valid timezone string.
    """
    data = load_user_timezones()
    timezone = data.get(str(chat_id), DEFAULT_TIMEZONE)
    if timezone not in all_timezones:
        logger.warning(f"⚠️ [TimezoneManager] Invalid stored timezone for {chat_id}: {timezone}. Falling back to UTC.")
        return DEFAULT_TIMEZONE
    return timezone

def set_user_timezone(chat_id: int, timezone: str) -> bool:
    """
    Sets a valid timezone for the user.

    Args:
        chat_id (int): Telegram Chat ID.
        timezone (str): Timezone string from pytz.

    Returns:
        bool: True if success, False otherwise.
    """
    if timezone not in all_timezones:
        logger.warning(f"⚠️ [TimezoneManager] Invalid timezone attempt: {timezone}")
        return False

    data = load_user_timezones()
    data[str(chat_id)] = timezone
    save_user_timezones(data)
    logger.info(f"✅ [TimezoneManager] Timezone set for {chat_id}: {timezone}")
    return True

def list_available_timezones() -> List[str]:
    """
    Returns sorted list of all supported timezones.

    Returns:
        List[str]: Timezones.
    """
    return sorted(all_timezones)
