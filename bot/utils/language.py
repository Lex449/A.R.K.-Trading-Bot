from telegram import Update

def get_language(update: Update) -> str:
    """Ermittelt die Sprache des Benutzers (Deutsch oder Englisch)."""
    lang = update.message.from_user.language_code

    # Falls die Sprache Deutsch oder Englisch ist, gebe die Sprache zurück, ansonsten Englisch als Standard.
    if lang in ['de', 'en']:
        return lang
    return 'en'  # Standard ist Englisch, wenn eine unbekannte Sprache erkannt wird.
