# bot/utils/language.py

"""
A.R.K. Language Manager – Ultra Stable Multilingual Engine 2025.
Handles user language preferences safely, scalable, and future-proof.
"""

import os
import json
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Path to store user language preferences
LANGUAGE_FILE = "user_language.json"

# In-memory cache
user_languages = {}

# === Helper Functions ===

def _load_languages():
    global user_languages
    if os.path.exists(LANGUAGE_FILE):
        try:
            with open(LANGUAGE_FILE, "r", encoding="utf-8") as f:
                user_languages = json.load(f)
            logger.info(f"✅ [LanguageManager] Loaded {len(user_languages)} user language settings.")
        except Exception as e:
            logger.error(f"❌ [LanguageManager] Failed to load user languages: {e}")

def _save_languages():
    try:
        with open(LANGUAGE_FILE, "w", encoding="utf-8") as f:
            json.dump(user_languages, f, ensure_ascii=False, indent=4)
        logger.info("✅ [LanguageManager] User languages saved successfully.")
    except Exception as e:
        logger.error(f"❌ [LanguageManager] Failed to save user languages: {e}")

# === Public Interface ===

def get_language(chat_id: int) -> str:
    """
    Returns the preferred language of a user.
    Defaults to English ("en") if unknown.
    """
    if not user_languages:
        _load_languages()

    return user_languages.get(str(chat_id), "en")

def set_language(chat_id: int, language_code: str):
    """
    Sets the preferred language for a user.
    """
    if language_code not in ["en", "de"]:
        logger.warning(f"⚠️ [LanguageManager] Unsupported language code '{language_code}'. Defaulting to 'en'.")
        language_code = "en"

    user_languages[str(chat_id)] = language_code
    _save_languages()
    logger.info(f"✅ [LanguageManager] Language set to '{language_code}' for chat_id {chat_id}.")
