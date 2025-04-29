# bot/utils/language.py

"""
A.R.K. Language Manager – Ultra Premium Multilingual System 2025.
Handles user-specific language preferences for a seamless experience.
"""

import os
import json
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Language Storage File ===
LANGUAGE_FILE = "user_languages.json"

# === Internal Memory ===
_user_languages = {}

def load_languages():
    """Loads user language settings from JSON file."""
    global _user_languages
    if os.path.exists(LANGUAGE_FILE):
        try:
            with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
                _user_languages = json.load(f)
                logger.info(f"✅ [LanguageManager] Loaded {len(_user_languages)} user languages.")
        except Exception as e:
            logger.error(f"❌ [LanguageManager] Failed to load languages: {e}")
            _user_languages = {}
    else:
        _user_languages = {}

def save_languages():
    """Saves user language settings to JSON file."""
    try:
        with open(LANGUAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(_user_languages, f, indent=4)
            logger.info("✅ [LanguageManager] User languages saved.")
    except Exception as e:
        logger.error(f"❌ [LanguageManager] Failed to save languages: {e}")

def get_language(chat_id: int) -> str:
    """Gets the saved language of a user."""
    try:
        return _user_languages.get(str(chat_id), "en")
    except Exception as e:
        logger.error(f"❌ [LanguageManager] Failed to get language: {e}")
        return "en"

def set_language(chat_id: int, lang: str) -> None:
    """Sets the language for a user."""
    try:
        _user_languages[str(chat_id)] = lang
        save_languages()
        logger.info(f"✅ [LanguageManager] Language updated for Chat ID {chat_id}: {lang}")
    except Exception as e:
        logger.error(f"❌ [LanguageManager] Failed to set language: {e}")

# === Initialize ===
load_languages()
