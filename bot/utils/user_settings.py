"""
A.R.K. User Settings Manager – Ultra Premium Build.
Manages per-user timezones and future settings cleanly.
"""

import json
import os
from typing import Dict

# === Settings File Path ===
USER_SETTINGS_FILE = "user_settings.json"

# === Internal Memory ===
_user_settings: Dict[int, dict] = {}

def load_user_settings():
    """Loads user settings from file."""
    global _user_settings
    if os.path.exists(USER_SETTINGS_FILE):
        try:
            with open(USER_SETTINGS_FILE, "r", encoding="utf-8") as f:
                _user_settings = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load user settings: {e}")
            _user_settings = {}
    else:
        _user_settings = {}

def save_user_settings():
    """Saves current user settings to file."""
    try:
        with open(USER_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(_user_settings, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"⚠️ Failed to save user settings: {e}")

def get_timezone(chat_id: int) -> str:
    """Retrieves the saved timezone for a user."""
    user_data = _user_settings.get(str(chat_id))
    if user_data:
        return user_data.get("timezone", "UTC")
    return "UTC"

def set_timezone(chat_id: int, timezone: str):
    """Sets the timezone for a user."""
    _user_settings[str(chat_id)] = {
        "timezone": timezone
    }
    save_user_settings()

def get_all_users() -> Dict[int, dict]:
    """Returns all user settings."""
    return _user_settings
