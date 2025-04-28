"""
A.R.K. Internationalization (i18n) Module – Ultra Premium Multilingual Build.
Handles multilingual text output for clean and scalable user interaction.
"""

import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Translation mappings ===
translations = {
    "en": {
        "start": "👋 Hello {user}! Welcome to *A.R.K. Trading Bot 2.0*.\n\nUse /help to view available commands and start trading smarter.",
        "help": "ℹ️ *Available Commands:*\n\n/start – Start the bot\n/help – Command overview\n/analyse [symbol] – Analyze a symbol (e.g., /analyse AAPL)\n/setlanguage [en/de] – Change language\n/signal – Get current trading signals\n/status – Show session statistics\n/shutdown – Stop the bot",
        "analysis_no_symbol": "❌ Please provide a valid symbol. Example: `/analyse AAPL`",
        "set_language": "✅ Language updated successfully. All future messages will be sent in your selected language.",
        "shutdown": "🛑 Bot is shutting down. Stay tuned for the next session!",
        # Session Tracker Additions
        "session_title_total": "📊 *Session Overview*",
        "session_title_today": "🌞 *Today’s Report*",
        "session_title_week": "📆 *Weekly Report*",
        "session_id": "Session ID",
        "start_time": "Start Time",
        "uptime": "Uptime",
        "total_signals": "Total Signals",
        "strong_signals": "Strong Signals (≥4⭐)",
        "moderate_signals": "Moderate Signals (3⭐)",
        "weak_signals": "Weak Signals (≤2⭐)",
        "avg_confidence": "Avg Confidence",
        "avg_score": "Avg Signal Score",
        "relentless_footer": "Relentless progress. Relentless precision."
    },
    "de": {
        "start": "👋 Hallo {user}! Willkommen bei *A.R.K. Trading Bot 2.0*.\n\nNutze /help, um alle verfügbaren Befehle anzuzeigen und smarter zu traden.",
        "help": "ℹ️ *Verfügbare Befehle:*\n\n/start – Bot starten\n/help – Befehlsübersicht\n/analyse [Symbol] – Ein Symbol analysieren (z.B. /analyse AAPL)\n/setlanguage [de/en] – Sprache ändern\n/signal – Aktuelle Handelssignale abrufen\n/status – Session-Statistik anzeigen\n/shutdown – Bot stoppen",
        "analysis_no_symbol": "❌ Bitte gib ein gültiges Symbol an. Beispiel: `/analyse AAPL`",
        "set_language": "✅ Sprache erfolgreich aktualisiert. Alle weiteren Nachrichten folgen in der gewählten Sprache.",
        "shutdown": "🛑 Der Bot wird beendet. Bis zum nächsten Einsatz!",
        # Session Tracker Additions
        "session_title_total": "📊 *Session Übersicht*",
        "session_title_today": "🌞 *Bericht Heute*",
        "session_title_week": "📆 *Wochenbericht*",
        "session_id": "Session-ID",
        "start_time": "Startzeit",
        "uptime": "Laufzeit",
        "total_signals": "Gesamtsignale",
        "strong_signals": "Starke Signale (≥4⭐)",
        "moderate_signals": "Moderate Signale (3⭐)",
        "weak_signals": "Schwache Signale (≤2⭐)",
        "avg_confidence": "Durchschnittliches Vertrauen",
        "avg_score": "Durchschnittliche Bewertung",
        "relentless_footer": "Unaufhaltsamer Fortschritt. Unaufhaltsame Präzision."
    }
}

SUPPORTED_LANGUAGES = ["en", "de"]

def get_text(key: str, lang: str = "en") -> str:
    """
    Retrieves the localized text for a given key and language.

    Args:
        key (str): The translation key.
        lang (str): Language code ('en', 'de').

    Returns:
        str: Translated text or fallback text if missing.
    """
    try:
        if lang not in SUPPORTED_LANGUAGES:
            logger.warning(f"[i18n] Unsupported language '{lang}'. Falling back to 'en'.")
            lang = "en"

        lang_data = translations.get(lang, translations["en"])
        text = lang_data.get(key)

        if text:
            return text
        else:
            logger.warning(f"[i18n] Missing text key '{key}' in language '{lang}'.")
            return f"🔍 Missing translation for key: `{key}`"

    except Exception as e:
        logger.error(f"[i18n] Critical error during text lookup: {e}")
        return f"🔍 Translation error for key: `{key}`"
