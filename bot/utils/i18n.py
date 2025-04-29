# bot/utils/i18n.py

"""
A.R.K. Internationalization (i18n) Engine – Human-Grade Localization.
Provides full multilingual translations for all core functions.
Made in Bali. Engineered with German Precision.
"""

import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

translations = {
    "en": {
        "start": "👋 Hello {user}! Welcome to *A.R.K. Trading Bot 2.0*.\nUse /help to see available features.",
        "help": "ℹ️ *Available Commands:* /start /help /analyse /signal /status /uptime /setlanguage /shutdown",
        "shutdown": "🛑 Bot is shutting down. See you soon!",
        "analysis_no_symbol": "❌ Please provide a symbol. Example: /analyse AAPL",
        "set_language": "✅ Language updated successfully!",
        "global_error_report": "⚠️ Unexpected error occurred:\n\n`{error}`",

        "no_data_today": "No data recorded today.",
        "signals_total": "Total Signals",
        "strong_signals": "Strong Signals",
        "moderate_signals": "Moderate Signals",
        "weak_signals": "Weak Signals",
        "avg_confidence": "Avg. Confidence",
        "summary_failed": "Summary generation failed.",
        "daily_recap": "Daily Recap",
        "weekly_recap": "Weekly Recap"
    },
    "de": {
        "start": "👋 Hallo {user}! Willkommen bei *A.R.K. Trading Bot 2.0*.\nVerwende /help, um die Funktionen anzuzeigen.",
        "help": "ℹ️ *Verfügbare Befehle:* /start /help /analyse /signal /status /uptime /setlanguage /shutdown",
        "shutdown": "🛑 Bot wird heruntergefahren. Bis bald!",
        "analysis_no_symbol": "❌ Bitte gib ein Symbol an. Beispiel: /analyse AAPL",
        "set_language": "✅ Sprache erfolgreich geändert!",
        "global_error_report": "⚠️ Unerwarteter Fehler aufgetreten:\n\n`{error}`",

        "no_data_today": "Keine Daten für heute erfasst.",
        "signals_total": "Signale insgesamt",
        "strong_signals": "Starke Signale",
        "moderate_signals": "Mittlere Signale",
        "weak_signals": "Schwache Signale",
        "avg_confidence": "Ø Vertrauensscore",
        "summary_failed": "Zusammenfassung fehlgeschlagen.",
        "daily_recap": "Tägliche Zusammenfassung",
        "weekly_recap": "Wöchentliche Zusammenfassung"
    }
}

SUPPORTED_LANGUAGES = ["en", "de"]

def get_text(key: str, lang: str = "en") -> str:
    """
    Fetches translated text safely.

    Args:
        key (str): Translation key.
        lang (str): Language code.

    Returns:
        str: Localized text.
    """
    try:
        if lang not in SUPPORTED_LANGUAGES:
            logger.warning(f"[i18n] Unsupported language '{lang}', fallback to English.")
            lang = "en"

        return translations.get(lang, {}).get(key, f"⚠️ Missing translation: {key}")

    except Exception as e:
        logger.error(f"[i18n] Fatal translation error: {e}")
        return f"⚠️ Translation Error: {key}"
