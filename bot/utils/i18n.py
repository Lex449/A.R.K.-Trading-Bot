TEXTS = {
    "start": {
        "en": "Welcome, {user}, to the A.R.K. Trading Bot!",
        "de": "Willkommen, {user}, beim A.R.K. Trading-Bot!"
    },
    "help": {
        "en": "Use /analyse <Symbol> to get an analysis. Set language with /setlanguage [de|en].",
        "de": "Verwende /analyse <Symbol> für eine Analyse. Sprache mit /setlanguage [de|en] einstellen."
    },
    "analysis_no_symbol": {
        "en": "Please provide a symbol to analyse (e.g. /analyse AAPL).",
        "de": "Bitte gib ein Symbol für die Analyse an (z.B. /analyse AAPL)."
    },
    "analysis_error": {
        "en": "Could not retrieve data for symbol {symbol}.",
        "de": "Daten für Symbol {symbol} konnten nicht abgerufen werden."
    },
    "set_language": {
        "en": "Language set successfully.",
        "de": "Sprache wurde erfolgreich gesetzt."
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """Gibt den Text für den gegebenen Schlüssel in der gewünschten Sprache zurück."""
    if key in TEXTS:
        return TEXTS[key].get(lang, TEXTS[key].get("en", ""))
    return ""