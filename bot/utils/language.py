# bot/utils/language.py

"""
Language detection and management module.
Determines user language preference with intelligent fallback.
"""

import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def get_language(update_or_context) -> str:
    """
    Determines the preferred language of the user.
    
    Priority:
    1. Checks if user_data['lang'] exists (context-based).
    2. Defaults to English ('en') if undefined or error.

    Args:
        update_or_context: Telegram Update object or chat ID/context.

    Returns:
        str: Language code ('en' or 'de').
    """
    try:
        if hasattr(update_or_context, "user_data"):
            lang = update_or_context.user_data.get("lang", "en")
            logger.debug(f"Language detected: {lang}")
            return lang
        else:
            logger.debug("Language defaulted to 'en' (no user_data).")
            return "en"

    except Exception as e:
        logger.error(f"Language detection error: {e}")
        return "en"
