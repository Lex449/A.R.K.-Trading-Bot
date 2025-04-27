"""
A.R.K. Timezone Manager – Global Ultra Build.
Handles user-specific timezones for full worldwide coverage.
"""

import pytz
import json
import os

# === User Settings File ===
USER_SETTINGS_FILE = "user_settings.json"

# === Default Timezone (Fallback) ===
DEFAULT_TIMEZONE = "Asia/Makassar"  # Bali Timezone (WITA)

# === Load user settings memory ===
_user_settings = {}

if os.path.exists(USER_SETTINGS_FILE):
    with open(USER_SETTINGS_FILE, "r", encoding="utf-8") as f:
        _user_settings = json.load(f)

def get_user_timezone(chat_id: int) -> str:
    """
    Returns the timezone for a specific user.
    Fallbacks to DEFAULT_TIMEZONE if not set.
    """
    chat_id = str(chat_id)
    return _user_settings.get(chat_id, {}).get("timezone", DEFAULT_TIMEZONE)

def set_user_timezone(chat_id: int, timezone: str) -> bool:
    """
    Sets a timezone for a specific user if valid.
    Returns True if successful, False if invalid.
    """
    if timezone not in pytz.all_timezones:
        return False

    chat_id = str(chat_id)
    if chat_id not in _user_settings:
        _user_settings[chat_id] = {}

    _user_settings[chat_id]["timezone"] = timezone

    _save_settings()
    return True

def _save_settings():
    """Persists current user settings to disk."""
    with open(USER_SETTINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(_user_settings, f, indent=4)

def list_available_timezones() -> list:
    """
    Returns a sorted list of all available pytz timezones.
    """
    return sorted(pytz.all_timezones)
