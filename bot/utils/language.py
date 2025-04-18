# bot/utils/language.py

from telegram import Update

def get_language(update: Update) -> str:
    """Ermittelt die Sprache des Benutzers (Deutsch oder Englisch)."""
    lang = update.message.from_user.language_code

    if lang in ['de', 'en']:
        return lang
    return 'en'  # Standard ist Englisch, wenn eine unbekannte Sprache erkannt wird.
