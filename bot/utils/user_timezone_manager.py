# bot/utils/user_timezone_manager.py

"""
A.R.K. User Timezone Manager – Ultra Global Build.
Handles individual user-specific timezones with full validation and persistence.
"""

import json
import os
from typing import Dict, List
from pytz import all_timezones
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === File to store user timezones ===
USER_TIMEZONE_FILE = "user_timezones.json"

def load_user_timezones() -> Dict[str, str]:
    """
    Loads user timezone mappings from file.

    Returns:
        Dict[str, str]: Mapping of chat IDs to timezone strings.
    """
    if os.path.exists(USER_TIMEZONE_FILE):
        try:
            with open(USER_TIMEZONE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.info("[Timezone Manager] User timezones loaded successfully.")
                return data
        except Exception as e:
            logger.warning(f"[Timezone Manager] Failed to load user timezones: {e}")
            return {}
    return {}

def save_user_timezones(data: Dict[str, str]) -> None:
    """
    Saves user timezone mappings to file.

    Args:
        data (Dict[str, str]): Mapping of chat IDs to timezone strings.
    """
    try:
        with open(USER_TIMEZONE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        logger.info("[Timezone Manager] User timezones saved successfully.")
    except Exception as e:
        logger.error(f"[Timezone Manager] Failed to save user timezones: {e}")

def set_user_timezone(chat_id: int, timezone: str) -> bool:
    """
    Sets the timezone for a specific user.

    Args:
        chat_id (int): Telegram chat ID.
        timezone (str): Valid timezone string.

    Returns:
        bool: True if timezone set successfully, False otherwise.
    """
    if timezone not in all_timezones:
        logger.warning(f"[Timezone Manager] Invalid timezone attempted: {timezone}")
        return False

    data = load_user_timezones()
    data[str(chat_id)] = timezone
    save_user_timezones(data)
    logger.info(f"[Timezone Manager] Timezone set for user {chat_id}: {timezone}")
    return True

def get_user_timezone(chat_id: int) -> str:
    """
    Retrieves the timezone for a specific user.

    Args:
        chat_id (int): Telegram chat ID.

    Returns:
        str: Timezone string (default: "UTC").
    """
    data = load_user_timezones()
    timezone = data.get(str(chat_id), "UTC")
    logger.debug(f"[Timezone Manager] Retrieved timezone for {chat_id}: {timezone}")
    return timezone

def list_available_timezones() -> List[str]:
    """
    Lists all available timezones.

    Returns:
        List[str]: Sorted list of timezone names.
    """
    return sorted(all_timezones)
