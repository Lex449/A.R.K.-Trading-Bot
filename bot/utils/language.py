# bot/utils/language.py

import logging
from telegram import Update

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Supported languages and their fallback mapping
SUPPORTED_LANGUAGES = {
    "de": "de", "de-de": "de", "de-at": "de", "de-ch": "de",
    "en": "en", "en-us": "en", "en-gb": "en"
}

def get_language(update: Update) -> str:
    """
    Detects the user's preferred language based on their Telegram settings.
    Supported languages: 'en', 'de'. Fallback is 'en' if detection fails.

    Args:
        update (Update): Telegram update containing user info.

    Returns:
        str: Language code ('en' or 'de').
    """
    try:
        raw_code = update.effective_user.language_code
        if not raw_code:
            logger.warning("No language code found. Defaulting to 'en'.")
            return "en"

        lang_code = raw_code.lower().strip()
        detected_language = SUPPORTED_LANGUAGES.get(lang_code, "en")

        logger.info(f"Language detected: '{lang_code}' → Using: '{detected_language}'")
        return detected_language

    except Exception as e:
        logger.error(f"Language detection error: {str(e)}")
        return "en"  # Always fallback to English on errors
