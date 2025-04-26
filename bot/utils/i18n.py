# bot/utils/i18n.py

TEXTS = {
    "start": {
        "en": "Welcome {user}! Ready to catch the next big move?\nUse `/analyse SYMBOL` to get started.",
        "de": "Willkommen {user}! Bereit für den nächsten großen Move?\nNutze `/analyse SYMBOL`, um zu starten."
    },
    "help": {
        "en": "🧠 *Available Commands:*\n"
              "`/start` – Welcome Message\n"
              "`/analyse SYMBOL` – Analyse a market\n"
              "`/help` – Show this help\n"
              "`/setlanguage de|en` – Change bot language",
        "de": "🧠 *Verfügbare Befehle:*\n"
              "`/start` – Begrüßung\n"
              "`/analyse SYMBOL` – Markt analysieren\n"
              "`/help` – Hilfe anzeigen\n"
              "`/setlanguage de|en` – Sprache ändern"
    },
    "analysis_no_symbol": {
        "en": "⚠️ Please provide a symbol (e.g., `/analyse US100`).",
        "de": "⚠️ Bitte gib ein Symbol an (z.B. `/analyse US100`)."
    },
    "analysis_error": {
        "en": "❌ Analysis failed for `{symbol}`. Please try again later.",
        "de": "❌ Analyse für `{symbol}` fehlgeschlagen. Bitte versuche es später erneut."
    },
    "set_language": {
        "en": "✅ Language updated successfully!",
        "de": "✅ Sprache erfolgreich geändert!"
    },
    "autoscaler_active": {
        "en": "🚀 *Auto-Scaler Activated*\nNew symbols added to maximize market coverage.",
        "de": "🚀 *Auto-Scaler Aktiviert*\nNeue Symbole hinzugefügt für maximale Marktabdeckung."
    },
    "autoscaler_nochange": {
        "en": "✅ *Auto-Scaler Check*\nAll symbols are already optimally configured.",
        "de": "✅ *Auto-Scaler Check*\nAlle Symbole sind bereits optimal eingestellt."
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """
    Retrieve the appropriate text string based on the provided key and language.
    If the language or key is not found, fallback to English.
    
    Args:
        key (str): The lookup key for the text.
        lang (str): The language code ('en' by default).
    
    Returns:
        str: The corresponding localized text or a fallback notice.
    """
    # First try to get the text in the requested language
    language_pack = TEXTS.get(key)
    if not language_pack:
        return "⚠️ Text not found."

    return language_pack.get(lang, language_pack.get("en", "⚠️ Text not available."))
