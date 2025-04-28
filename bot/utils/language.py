# bot/utils/language.py

"""
A.R.K. Language Detection and Management – Ultra Premium Build.
Determines user language preference with intelligent fallback system.
"""

import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Supported Languages ===
SUPPORTED_LANGUAGES = ["en", "de"]

def get_language(update_or_context) -> str:
    """
    Determines the preferred language of the user.
    
    Priority:
    1. Checks if user_data['lang'] exists (context-based).
    2. Defaults to English ('en') if undefined or invalid.

    Args:
        update_or_context: Telegram Update object, Context object, or fallback.

    Returns:
        str: Language code ('en' or 'de').
    """
    try:
        lang = "en"  # Default fallback

        if hasattr(update_or_context, "user_data"):
            lang_candidate = update_or_context.user_data.get("lang", "en")
            if lang_candidate in SUPPORTED_LANGUAGES:
                lang = lang_candidate
            else:
                logger.warning(f"[Language Manager] Unsupported language fallback: {lang_candidate}")

        logger.debug(f"[Language Manager] Detected language: {lang}")
        return lang

    except Exception as e:
        logger.error(f"[Language Manager] Language detection error: {e}")
        return "en"
