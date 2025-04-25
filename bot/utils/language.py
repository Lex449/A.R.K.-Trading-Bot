# bot/utils/language.py

from telegram import Update

SUPPORTED_LANGUAGES = {
    "de": "de",
    "de-de": "de",
    "de-at": "de",
    "de-ch": "de",
    "en": "en",
    "en-us": "en",
    "en-gb": "en"
}

def get_language(update: Update) -> str:
    """
    Erkennt die Nutzersprache anhand der Telegram-Spracheinstellung.
    Gibt 'de' für Deutsch oder 'en' für Englisch zurück.
    Fallback ist Englisch bei unbekannten oder fehlenden Codes.
    """
    try:
        lang_code = (update.effective_user.language_code or "").lower()
        return SUPPORTED_LANGUAGES.get(lang_code, "en")
    except Exception as e:
        print(f"[LANGUAGE WARNING] Sprach-Erkennung fehlgeschlagen: {e}")
        return "en"
