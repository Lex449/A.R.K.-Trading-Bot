"""
A.R.K. User Settings Manager – Ultra Premium Build.
Manages per-user timezones and future user-specific settings cleanly.
Made in Bali. Engineered with German Precision.
"""

import json
import os
from typing import Dict, Optional
from bot.utils.logger import setup_logger

# Logger Setup
logger = setup_logger(__name__)

# Constants
USER_SETTINGS_FILE = "user_settings.json"

# Internal Cache
_user_settings: Dict[str, dict] = {}

# === Core Persistence Layer ===

def load_user_settings() -> None:
    """Loads all user settings from disk into memory."""
    global _user_settings

    if os.path.exists(USER_SETTINGS_FILE):
        try:
            with open(USER_SETTINGS_FILE, "r", encoding="utf-8") as f:
                _user_settings = json.load(f)
            logger.info("✅ [UserSettings] Settings loaded successfully.")
        except Exception as e:
            logger.warning(f"⚠️ [UserSettings] Failed to load file: {e}")
            _user_settings = {}
    else:
        logger.info("ℹ️ [UserSettings] No settings file found. Initializing fresh state.")
        _user_settings = {}

def save_user_settings() -> None:
    """Saves current in-memory settings to disk."""
    try:
        with open(USER_SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(_user_settings, f, indent=4, ensure_ascii=False)
        logger.info("✅ [UserSettings] Settings saved successfully.")
    except Exception as e:
        logger.error(f"❌ [UserSettings] Failed to save settings: {e}")

# === Accessors ===

def get_timezone(chat_id: int) -> str:
    """Returns the user's saved timezone or default 'UTC'."""
    return _user_settings.get(str(chat_id), {}).get("timezone", "UTC")

def set_timezone(chat_id: int, timezone: str) -> None:
    """Sets a user's timezone setting and persists it."""
    chat_key = str(chat_id)
    if chat_key not in _user_settings:
        _user_settings[chat_key] = {}

    _user_settings[chat_key]["timezone"] = timezone
    save_user_settings()
    logger.info(f"✅ [UserSettings] Timezone updated for {chat_id}: {timezone}")

def get_all_users() -> Dict[str, dict]:
    """Returns all user profiles/settings."""
    return _user_settings

def get_user_settings(chat_id: int) -> Optional[dict]:
    """Returns full settings dict for user."""
    return _user_settings.get(str(chat_id))

def update_user_setting(chat_id: int, key: str, value) -> None:
    """Updates a single setting key for a user."""
    chat_key = str(chat_id)
    if chat_key not in _user_settings:
        _user_settings[chat_key] = {}

    _user_settings[chat_key][key] = value
    save_user_settings()
    logger.info(f"✅ [UserSettings] Updated {key} for {chat_id}: {value}")

# === Startup Init ===
load_user_settings()
