# bot/utils/user_settings_manager.py

"""
A.R.K. User Settings Manager – Ultra Premium Build.
Manages per-user timezones and future user-specific settings cleanly.
"""

import json
import os
from typing import Dict
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Settings File Path ===
USER_SETTINGS_FILE = "user_settings.json"

# === Internal Memory ===
_user_settings: Dict[str, dict] = {}

def load_user_settings() -> None:
    """Loads user settings from file."""
    global _user_settings
    if os.path.exists(USER_SETTINGS_FILE):
        try:
            with open(USER_SETTINGS_FILE, "r", encoding="utf-8") as f:
                _user_settings = json.load(f)
            logger.info("[User Settings] Loaded successfully.")
        except Exception as e:
            logger.warning(f"[User Settings] Failed to load settings: {e}")
            _user_settings = {}
    else:
        _user_settings = {}
        logger.info("[User Settings] No existing settings file found.")

def save_user_settings() -> None:
    """Saves current user settings to file."""
    try:
        with open(USER_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(_user_settings, f, indent=4, ensure_ascii=False)
        logger.info("[User Settings] Saved successfully.")
    except Exception as e:
        logger.error(f"[User Settings] Failed to save settings: {e}")

def get_timezone(chat_id: int) -> str:
    """Retrieves the saved timezone for a user.

    Args:
        chat_id (int): Telegram chat ID.

    Returns:
        str: Timezone string (default "UTC" if not set).
    """
    user_data = _user_settings.get(str(chat_id))
    if user_data:
        return user_data.get("timezone", "UTC")
    return "UTC"

def set_timezone(chat_id: int, timezone: str) -> None:
    """Sets the timezone for a user.

    Args:
        chat_id (int): Telegram chat ID.
        timezone (str): Timezone string.
    """
    _user_settings[str(chat_id)] = {
        "timezone": timezone
    }
    save_user_settings()

def get_all_users() -> Dict[str, dict]:
    """Returns all user settings.

    Returns:
        Dict[str, dict]: All user data.
    """
    return _user_settings
