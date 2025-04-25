# bot/utils/language.py

from telegram import Update

# Unterstützte Sprachen und ihre Fallbacks
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
        if raw_code is None:
            print("[LANGUAGE WARNING] Keine Sprache gefunden. Standard zu 'en'.")
            return "en"

        lang_code = raw_code.lower().strip()

        detected = SUPPORTED_LANGUAGES.get(lang_code, "en")  # Default auf Englisch, wenn Sprache nicht gefunden
        print(f"[LANGUAGE] Detected: '{lang_code}' → Using: '{detected}'")  # Debugging-Ausgabe
        return detected

    except Exception as e:
        print(f"[LANGUAGE ERROR] Fehler bei der Spracherkennung: {e}")  # Genauere Fehlerausgabe
        return "en"  # Fallback auf Englisch bei Fehlern
