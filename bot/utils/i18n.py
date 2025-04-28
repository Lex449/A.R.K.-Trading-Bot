"""
A.R.K. Internationalization (i18n) Engine – Ultra Premium Localization Build.
Handles multilingual support for all bot interactions. 
Maximal fault-tolerant, scalable, human-grade translations.
"""

import logging
from bot.utils.logger import setup_logger

# Setup Structured Logger
logger = setup_logger(__name__)

# === Supported Translations ===
translations = {
    "en": {
        "start": "👋 Hello {user}! Welcome to *A.R.K. Trading Bot 2.0*.\n\nUse /help to explore smart trading commands.",
        "start_help_hint": "ℹ️ Tip: Use /help anytime to see available features.",
        "help": "ℹ️ *Available Commands:*\n\n/start – Start Bot\n/help – Commands Overview\n/analyse [symbol] – Analyze a symbol (e.g., /analyse AAPL)\n/setlanguage [en/de] – Change Language\n/signal – Live Trading Signals\n/status – Current Trading Session Stats\n/shutdown – Shut Down Bot",
        "analysis_no_symbol": "❌ Please provide a valid symbol. Example: `/analyse AAPL`",
        "set_language": "✅ Language updated successfully!",
        "shutdown": "🛑 Bot is shutting down. See you soon!",
        "fetching_data_primary": "Fetching market data from primary source (Finnhub)...",
        "fetching_data_backup": "Primary source failed. Switching to backup (Yahoo Finance)...",
        "error_primary_source": "Primary source error (Finnhub).",
        "error_backup_source": "Backup source error (Yahoo Finance).",
        "analysis_completed": "✅ Analysis completed!",
        "session_title_total": "📊 *Session Overview*",
        "session_title_today": "🌞 *Today’s Results*",
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
        "relentless_footer": "Relentless focus. Relentless progress.",
        "signal_ultra_premium": "Ultra Premium Signal Generated",
        "signal_footer": "Smart trading starts with smart signals."
    },
    "de": {
        "start": "👋 Hallo {user}! Willkommen bei *A.R.K. Trading Bot 2.0*.\n\nNutze /help, um alle Funktionen zu entdecken.",
        "start_help_hint": "ℹ️ Tipp: Nutze /help jederzeit für eine Übersicht.",
        "help": "ℹ️ *Verfügbare Befehle:*\n\n/start – Bot starten\n/help – Befehlsübersicht\n/analyse [Symbol] – Symbol analysieren (z.B. /analyse AAPL)\n/setlanguage [de/en] – Sprache ändern\n/signal – Live Handelssignale\n/status – Aktuelle Session-Statistiken\n/shutdown – Bot stoppen",
        "analysis_no_symbol": "❌ Bitte ein gültiges Symbol angeben. Beispiel: `/analyse AAPL`",
        "set_language": "✅ Sprache erfolgreich geändert!",
        "shutdown": "🛑 Bot wird beendet. Bis bald!",
        "fetching_data_primary": "Marktdaten von Primärquelle (Finnhub) werden geladen...",
        "fetching_data_backup": "Primärquelle fehlgeschlagen. Wechsel zur Backup-Quelle (Yahoo Finance)...",
        "error_primary_source": "Fehler bei Finnhub-Daten.",
        "error_backup_source": "Fehler bei Yahoo Finance-Daten.",
        "analysis_completed": "✅ Analyse erfolgreich abgeschlossen!",
        "session_title_total": "📊 *Session Übersicht*",
        "session_title_today": "🌞 *Heutige Ergebnisse*",
        "session_title_week": "📆 *Wochenbericht*",
        "session_id": "Session-ID",
        "start_time": "Startzeit",
        "uptime": "Laufzeit",
        "total_signals": "Gesamtsignale",
        "strong_signals": "Starke Signale (≥4⭐)",
        "moderate_signals": "Moderate Signale (3⭐)",
        "weak_signals": "Schwache Signale (≤2⭐)",
        "avg_confidence": "Ø Vertrauen",
        "avg_score": "Ø Signalbewertung",
        "relentless_footer": "Unaufhaltsamer Fokus. Unaufhaltsamer Fortschritt.",
        "signal_ultra_premium": "Ultra Premium Signal erkannt",
        "signal_footer": "Smartes Trading beginnt mit smarten Signalen."
    }
}

SUPPORTED_LANGUAGES = ["en", "de"]

def get_text(key: str, lang: str = "en") -> str:
    """
    Fetches the localized text for a given key and language safely.

    Args:
        key (str): Text key to translate.
        lang (str): Language code ('en', 'de').

    Returns:
        str: Translated string, or fallback string if missing.
    """
    try:
        if lang not in SUPPORTED_LANGUAGES:
            logger.warning(f"[i18n] Unsupported language '{lang}'. Fallback to English.")
            lang = "en"

        lang_data = translations.get(lang, translations["en"])
        text = lang_data.get(key)

        if text:
            return text
        else:
            logger.warning(f"[i18n] Missing key '{key}' in '{lang}' translations.")
            return f"🔍 Missing translation for `{key}`"

    except Exception as e:
        logger.error(f"[i18n] Fatal translation lookup error: {e}")
        return f"⚠️ Translation Error for `{key}`"
