"""
A.R.K. Language Manager – Ultra Multilingual Switcher
Handles user language settings dynamically and persistently.
"""

import os
import json
from bot.utils.logger import setup_logger

# Setup Structured Logger
logger = setup_logger(__name__)

# === File for storing user language preferences ===
LANGUAGE_FILE = "user_languages.json"

# === Internal Memory ===
user_languages = {}

def load_user_languages() -> None:
    """
    Loads all user language settings from disk.
    """
    global user_languages

    if os.path.exists(LANGUAGE_FILE):
        try:
            with open(LANGUAGE_FILE, "r", encoding="utf-8") as file:
                user_languages = json.load(file)
            logger.info("✅ [LanguageManager] User languages loaded successfully.")
        except Exception as e:
            logger.error(f"❌ [LanguageManager] Failed to load user languages: {e}")
            user_languages = {}
    else:
        user_languages = {}

def save_user_languages() -> None:
    """
    Saves all user language settings to disk.
    """
    try:
        with open(LANGUAGE_FILE, "w", encoding="utf-8") as file:
            json.dump(user_languages, file, indent=4)
        logger.info("✅ [LanguageManager] User languages saved successfully.")
    except Exception as e:
        logger.error(f"❌ [LanguageManager] Failed to save user languages: {e}")

def set_language(chat_id: int, language: str) -> None:
    """
    Sets the language preference for a specific user.

    Args:
        chat_id (int): The user's chat ID.
        language (str): Language code (e.g., 'en', 'de').
    """
    global user_languages
    user_languages[str(chat_id)] = language
    save_user_languages()
    logger.info(f"🌐 [LanguageManager] Language for chat_id {chat_id} set to {language}.")

def get_language(chat_id: int) -> str:
    """
    Gets the language preference for a specific user.

    Args:
        chat_id (int): The user's chat ID.

    Returns:
        str: The user's language code ('en' by default if not set).
    """
    return user_languages.get(str(chat_id), "en")
