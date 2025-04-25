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
        "en": "⚠️ Please provide a symbol (e.g. `/analyse US100`).",
        "de": "⚠️ Bitte gib ein Symbol an (z.B. `/analyse US100`)."
    },
    "analysis_error": {
        "en": "❌ Analysis failed for `{symbol}`. Please try again later.",
        "de": "❌ Analyse für `{symbol}` fehlgeschlagen. Bitte später erneut versuchen."
    },
    "set_language": {
        "en": "✅ Language updated successfully!",
        "de": "✅ Sprache erfolgreich geändert!"
    },
    "autoscaler_active": {
        "en": "🚀 *Auto-Scaler activated:*\nNew symbols added to maximize coverage.",
        "de": "🚀 *Auto-Scaler aktiviert:*\nNeue Symbole hinzugefügt für maximale Abdeckung."
    },
    "autoscaler_nochange": {
        "en": "✅ *Auto-Scaler Check:*\nAll symbols already optimal.",
        "de": "✅ *Auto-Scaler Check:*\nAlle Symbole sind bereits optimal eingestellt."
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """
    Holt den passenden Text zum Schlüssel, abhängig von der Sprache.
    Fallback: Englisch, wenn Sprache oder Key fehlt.
    """
    return TEXTS.get(key, {}).get(lang) or TEXTS.get(key, {}).get("en", "")
