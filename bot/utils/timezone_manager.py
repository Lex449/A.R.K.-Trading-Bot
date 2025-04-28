# bot/utils/timezone_manager.py

"""
A.R.K. Timezone Manager – Global Ultra Build.
Handles user-specific timezones for full worldwide coverage.
"""

import pytz
import json
import os
from json import JSONDecodeError
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === User Settings File ===
USER_SETTINGS_FILE = "user_settings.json"

# === Default Timezone (Fallback) ===
DEFAULT_TIMEZONE = "Asia/Makassar"  # Bali Timezone (WITA)

# === Load user settings memory ===
_user_settings = {}

if os.path.exists(USER_SETTINGS_FILE):
    try:
        with open(USER_SETTINGS_FILE, "r", encoding="utf-8") as f:
            _user_settings = json.load(f)
    except (JSONDecodeError, Exception) as e:
        logger.warning(f"⚠️ [Timezone Manager] Failed to load user_settings.json: {e}")
        _user_settings = {}

def get_user_timezone(chat_id: int) -> str:
    """
    Returns the timezone for a specific user.
    Fallbacks to DEFAULT_TIMEZONE if not set.

    Args:
        chat_id (int): Telegram chat ID.

    Returns:
        str: Timezone string.
    """
    chat_id = str(chat_id)
    return _user_settings.get(chat_id, {}).get("timezone", DEFAULT_TIMEZONE)

def set_user_timezone(chat_id: int, timezone: str) -> bool:
    """
    Sets a timezone for a specific user if valid.
    
    Args:
        chat_id (int): Telegram chat ID.
        timezone (str): Valid timezone string.

    Returns:
        bool: True if timezone set successfully, False otherwise.
    """
    if timezone not in pytz.all_timezones:
        return False

    chat_id = str(chat_id)
    if chat_id not in _user_settings:
        _user_settings[chat_id] = {}

    _user_settings[chat_id]["timezone"] = timezone
    _save_settings()
    return True

def _save_settings() -> None:
    """Persists current user settings to disk."""
    with open(USER_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(_user_settings, f, indent=4)

def list_available_timezones() -> list[str]:
    """
    Returns a sorted list of all available pytz timezones.

    Returns:
        list[str]: List of timezone names.
    """
    return sorted(pytz.all_timezones)
