# bot/utils/language.py

from telegram import Update

SUPPORTED_LANGUAGES = {
    "de": "de", "de-de": "de", "de-at": "de", "de-ch": "de",
    "en": "en", "en-us": "en", "en-gb": "en"
}

def get_language(update: Update) -> str:
    """
    Erkennt die Sprache des Nutzers basierend auf Telegram-Spracheinstellung.
    Unterstützt aktuell: 'de', 'en'.
    Fallback: 'en'
    """
    try:
        raw_code = update.effective_user.language_code
        lang_code = (raw_code or "").lower().strip()

        detected = SUPPORTED_LANGUAGES.get(lang_code, "en")
        print(f"[LANGUAGE] Detected: '{lang_code}' → Using: '{detected}'")
        return detected

    except Exception as e:
        print(f"[LANGUAGE WARNING] Fehler bei Sprach-Erkennung: {e}")
        return "en"
