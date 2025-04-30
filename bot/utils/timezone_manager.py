"""
A.R.K. Timezone Manager – Global Ultra Masterclass Build.
Manages user-specific timezones across all continents with error resilience.
Made in Bali. Engineered with German Precision.
"""

import pytz
import json
import os
from json import JSONDecodeError
from bot.utils.logger import setup_logger

# === Logger Setup ===
logger = setup_logger(__name__)

# === Constants ===
USER_SETTINGS_FILE = "user_settings.json"
DEFAULT_TIMEZONE = "Asia/Makassar"  # Bali Timezone (WITA)

# === Internal Memory ===
_user_settings = {}

# === Initial Load ===
if os.path.exists(USER_SETTINGS_FILE):
    try:
        with open(USER_SETTINGS_FILE, "r", encoding="utf-8") as f:
            _user_settings = json.load(f)
            logger.info("✅ [TimezoneManager] Loaded existing timezone settings.")
    except (JSONDecodeError, Exception) as e:
        logger.warning(f"⚠️ [TimezoneManager] Corrupted settings file. Starting fresh. Error: {e}")
        _user_settings = {}
else:
    logger.info("ℹ️ [TimezoneManager] No timezone settings file found. Will create on first save.")

# === Core Functions ===

def get_user_timezone(chat_id: int) -> str:
    """
    Retrieves the timezone for a specific user. Falls back to default if unset/invalid.

    Args:
        chat_id (int): Telegram Chat ID.

    Returns:
        str: Timezone name (e.g., "Europe/Berlin").
    """
    try:
        chat_id = str(chat_id)
        tz = _user_settings.get(chat_id, {}).get("timezone", DEFAULT_TIMEZONE)

        if tz not in pytz.all_timezones:
            logger.warning(f"⚠️ [TimezoneManager] Invalid timezone '{tz}' for user {chat_id}. Resetting to default.")
            return DEFAULT_TIMEZONE

        return tz

    except Exception as e:
        logger.error(f"❌ [TimezoneManager] Failed to retrieve timezone for user {chat_id}: {e}")
        return DEFAULT_TIMEZONE

def set_user_timezone(chat_id: int, timezone: str) -> bool:
    """
    Assigns a valid timezone to a user.

    Args:
        chat_id (int): Telegram Chat ID.
        timezone (str): A valid timezone string (e.g., "Europe/London").

    Returns:
        bool: True on success, False if invalid timezone.
    """
    if timezone not in pytz.all_timezones:
        logger.warning(f"⚠️ [TimezoneManager] Invalid timezone attempted: {timezone}")
        return False

    chat_id = str(chat_id)
    if chat_id not in _user_settings:
        _user_settings[chat_id] = {}

    _user_settings[chat_id]["timezone"] = timezone
    _save_settings()
    logger.info(f"✅ [TimezoneManager] Timezone for {chat_id} set to {timezone}")
    return True

def list_available_timezones() -> list[str]:
    """
    Returns a sorted list of all available timezone names.

    Returns:
        list[str]: Timezone names.
    """
    return sorted(pytz.all_timezones)

def _save_settings() -> None:
    """
    Writes the user timezone settings to disk.
    """
    try:
        with open(USER_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(_user_settings, f, indent=4)
        logger.info("✅ [TimezoneManager] Timezone settings saved.")
    except Exception as e:
        logger.error(f"❌ [TimezoneManager] Failed to save settings: {e}")
