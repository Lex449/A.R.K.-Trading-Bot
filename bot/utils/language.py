# bot/utils/language.py

from telegram import Update

def get_language(update: Update) -> str:
    """
    Erkennt die Sprache des Benutzers anhand des Telegram-Profils.
    Gibt 'de' oder 'en' zurück. Standard ist Englisch.
    """
    try:
        lang_code = update.effective_user.language_code
        if lang_code and lang_code.lower().startswith("de"):
            return "de"
        else:
            return "en"
    except Exception:
        return "en"
