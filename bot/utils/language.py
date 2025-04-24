# bot/utils/language.py

from telegram import Update

def get_language(update: Update) -> str:
    """
    Bestimmt die bevorzugte Sprache des Nutzers auf Basis der Telegram-Spracheinstellung.

    Rückgabe:
        'de' – wenn Sprache auf Deutsch gesetzt ist.
        'en' – in allen anderen Fällen (inkl. Fallback).
    """
    try:
        lang_code = update.effective_user.language_code or ""
        return "de" if lang_code.lower().startswith("de") else "en"
    except Exception as e:
        print(f"[WARN] Language detection failed: {e}")
        return "en"
