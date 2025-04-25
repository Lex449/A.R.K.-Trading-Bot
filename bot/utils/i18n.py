# bot/utils/i18n.py

TEXTS = {
    "start": {
        "en": "Welcome {user}! Ready to catch the next big move? Use /analyse SYMBOL to start.",
        "de": "Willkommen {user}! Bereit für den nächsten großen Move? Nutze /analyse SYMBOL um zu starten."
    },
    "help": {
        "en": "Commands available:\n/start - Welcome Message\n/analyse SYMBOL - Analyse a market\n/help - Command Help\n/setlanguage de|en - Switch Language",
        "de": "Verfügbare Befehle:\n/start - Begrüßung\n/analyse SYMBOL - Markt analysieren\n/help - Hilfe anzeigen\n/setlanguage de|en - Sprache wechseln"
    },
    "analysis_no_symbol": {
        "en": "Please provide a symbol (e.g., /analyse US100).",
        "de": "Bitte gib ein Symbol an (z.B. /analyse US100)."
    },
    "analysis_error": {
        "en": "Analysis failed for {symbol}. Please try again later.",
        "de": "Analyse für {symbol} fehlgeschlagen. Bitte später erneut versuchen."
    },
    "set_language": {
        "en": "Language updated successfully!",
        "de": "Sprache erfolgreich geändert!"
    },
    "autoscaler_active": {
        "en": "Auto-Scaler activated: Added new symbols.",
        "de": "Auto-Scaler aktiviert: Neue Symbole hinzugefügt."
    },
    "autoscaler_nochange": {
        "en": "Auto-Scaler: Symbol setup already optimal.",
        "de": "Auto-Scaler: Symbolsetup bereits optimal."
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """
    Holt den übersetzten Text für den gegebenen Schlüssel.
    Fallback: Englisch, wenn Übersetzung fehlt.
    """
    return TEXTS.get(key, {}).get(lang, TEXTS.get(key, {}).get("en", ""))
