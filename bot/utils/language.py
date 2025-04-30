# bot/utils/language.py

"""
A.R.K. Language Manager – Ultra Resilient Multilingual Engine 2025.
Handles dynamic language preferences per user with fallback, logging and upgrade-ready persistence.

Made in Bali. Engineered with German Precision.
"""

import json
import os
from bot.utils.logger import setup_logger

# === Setup structured logger ===
logger = setup_logger(__name__)
LANGUAGE_FILE = "user_languages.json"

# === In-Memory Language Store ===
user_languages = {}

def load_language_preferences():
    """Loads language settings from disk if available."""
    global user_languages

    if os.path.exists(LANGUAGE_FILE):
        try:
            with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
                user_languages = json.load(f)
                logger.info("✅ [LanguageManager] Loaded language settings.")
        except Exception as e:
            logger.warning(f"⚠️ [LanguageManager] Failed to load settings: {e}")
            user_languages = {}
    else:
        user_languages = {}

def save_language_preferences():
    """Saves language preferences to disk."""
    try:
        with open(LANGUAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(user_languages, f, indent=2)
        logger.info("✅ [LanguageManager] Language settings saved.")
    except Exception as e:
        logger.error(f"❌ [LanguageManager] Failed to save language settings: {e}")

def get_language(chat_id: int) -> str:
    """
    Gets the preferred language for a user.

    Args:
        chat_id (int): Telegram chat ID.

    Returns:
        str: Language code ("en" or "de").
    """
    lang = user_languages.get(str(chat_id), "en")

    if lang not in ["en", "de"]:
        logger.warning(f"[LanguageManager] Invalid language fallback for user {chat_id}")
        return "en"

    return lang

def set_language(chat_id: int, lang: str):
    """
    Sets the preferred language for a user.

    Args:
        chat_id (int): Telegram chat ID.
        lang (str): Language code.
    """
    if lang not in ["en", "de"]:
        logger.warning(f"[LanguageManager] Invalid language code: {lang}")
        return

    user_languages[str(chat_id)] = lang
    logger.info(f"✅ [LanguageManager] Set language for {chat_id} → {lang}")
    save_language_preferences()

# === Auto-Load at startup ===
load_language_preferences()
