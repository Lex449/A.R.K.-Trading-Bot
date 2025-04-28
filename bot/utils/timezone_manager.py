"""
A.R.K. Timezone Manager – Global Ultra Masterclass Build.
Manages user-specific timezones across all continents with error resilience.
"""

import pytz
import json
import os
from json import JSONDecodeError
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Constants ===
USER_SETTINGS_FILE = "user_settings.json"
DEFAULT_TIMEZONE = "Asia/Makassar"  # Bali Timezone (WITA)

# === Internal User Settings Memory ===
_user_settings = {}

# === Load Settings on Startup ===
if os.path.exists(USER_SETTINGS_FILE):
    try:
        with open(USER_SETTINGS_FILE, "r", encoding="utf-8") as f:
            _user_settings = json.load(f)
            logger.info("✅ [Timezone Manager] user_settings.json loaded successfully.")
    except (JSONDecodeError, Exception) as e:
        logger.warning(f"⚠️ [Timezone Manager] Corrupted user_settings.json detected: {e}")
        _user_settings = {}
else:
    logger.info("ℹ️ [Timezone Manager] No existing user_settings.json found. New will be created on save.")

def get_user_timezone(chat_id: int) -> str:
    """
    Returns the configured timezone for a user.
    Defaults to Asia/Makassar if not set.

    Args:
        chat_id (int): Telegram Chat ID.

    Returns:
        str: Timezone string.
    """
    try:
        chat_id = str(chat_id)
        tz = _user_settings.get(chat_id, {}).get("timezone", DEFAULT_TIMEZONE)

        if tz not in pytz.all_timezones:
            logger.warning(f"⚠️ [Timezone Manager] Invalid timezone for user {chat_id}: {tz}. Reset to default.")
            return DEFAULT_TIMEZONE

        return tz

    except Exception as e:
        logger.error(f"❌ [Timezone Manager] Error retrieving timezone for user {chat_id}: {e}")
        return DEFAULT_TIMEZONE

def set_user_timezone(chat_id: int, timezone: str) -> bool:
    """
    Safely sets a valid timezone for a user.

    Args:
        chat_id (int): Telegram Chat ID.
        timezone (str): Timezone string.

    Returns:
        bool: True if successful, False otherwise.
    """
    if timezone not in pytz.all_timezones:
        logger.warning(f"⚠️ [Timezone Manager] Attempted to set invalid timezone: {timezone}")
        return False

    chat_id = str(chat_id)
    if chat_id not in _user_settings:
        _user_settings[chat_id] = {}

    _user_settings[chat_id]["timezone"] = timezone
    _save_settings()
    logger.info(f"✅ [Timezone Manager] Timezone for user {chat_id} set to {timezone}")
    return True

def _save_settings() -> None:
    """Saves all user timezone settings to disk."""
    try:
        with open(USER_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(_user_settings, f, indent=4)
        logger.info("✅ [Timezone Manager] User settings saved successfully.")
    except Exception as e:
        logger.error(f"❌ [Timezone Manager] Failed to save user settings: {e}")

def list_available_timezones() -> list[str]:
    """
    Returns all available pytz timezones in alphabetical order.

    Returns:
        list[str]: Available timezone names.
    """
    return sorted(pytz.all_timezones)
