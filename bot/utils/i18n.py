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
        "set_language": "✅ Language updated successfully!",
        "analysis_no_symbol": "❌ Please provide a symbol. Example: /analyse AAPL",
        "no_analysis_data": "❌ No valid analysis found for *{symbol}*.",
        "analyzing": "Analyzing",
        "analysis_completed": "Analysis Completed",
        "no_patterns_found": "No strong patterns found.",
        "live_signal_info": "⚡ *Live signals are sent automatically during trading hours. No need to use /signal manually.*",
        "summary_failed": "Summary generation failed.",
        "no_data_today": "No data recorded today.",
        "signals_total": "Total Signals",
        "strong_signals": "Strong Signals",
        "moderate_signals": "Moderate Signals",
        "weak_signals": "Weak Signals",
        "avg_confidence": "Avg. Confidence",
        "daily_recap": "Daily Recap",
        "weekly_recap": "Weekly Recap",
        "scan_start": "🔍 *Starting Auto-Analysis...*",
        "no_symbols_configured": "❌ No symbols configured for auto-analysis.",
        "no_signals_found": "ℹ️ *No trading signals detected during scan.*",
        "scan_complete_success": "✅ *Auto-Analysis Completed Successfully!*",
        "scan_complete_empty": "⚠️ *Scan completed – but no valid signals were generated.*",
        "global_error_report": "⚠️ Unexpected error occurred:\n\n`{error}`",

        # === Notifications ===
        "notification_title": "New {action} Signal",
        "symbol": "Symbol",
        "move": "Price Move",
        "volume_spike": "Volume Spike",
        "trend": "Trend",
        "confidence": "Confidence",
        "risk_reward": "Risk/Reward",
        "notification_confidence_ultra": "⭐️ *Elite Setup* – This is as good as it gets.",
        "notification_confidence_high": "🔍 *Strong Opportunity* – Validated by trend & volume.",
        "notification_confidence_moderate": "⚠️ *Moderate Setup* – Needs caution or confirmation.",
        "notification_confidence_low": "❌ *Weak Signal* – Avoid or monitor only.",
        "notification_footer": "_Analyze responsibly. No FOMO – only precision._"
    },
    "de": {
        "start": "👋 Hallo {user}! Willkommen bei *A.R.K. Trading Bot 2.0*.\nVerwende /help, um die Funktionen anzuzeigen.",
        "help": "ℹ️ *Verfügbare Befehle:* /start /help /analyse /signal /status /uptime /setlanguage /shutdown",
        "shutdown": "🛑 Bot wird heruntergefahren. Bis bald!",
        "set_language": "✅ Sprache erfolgreich geändert!",
        "analysis_no_symbol": "❌ Bitte gib ein Symbol an. Beispiel: /analyse AAPL",
        "no_analysis_data": "❌ Keine gültige Analyse gefunden für *{symbol}*.",
        "analyzing": "Analysiere",
        "analysis_completed": "Analyse abgeschlossen",
        "no_patterns_found": "Keine starken Muster erkannt.",
        "live_signal_info": "⚡ *Live-Signale werden automatisch während der Handelszeiten gesendet. /signal ist nicht nötig.*",
        "summary_failed": "Zusammenfassung fehlgeschlagen.",
        "no_data_today": "Keine Daten für heute erfasst.",
        "signals_total": "Signale insgesamt",
        "strong_signals": "Starke Signale",
        "moderate_signals": "Mittlere Signale",
        "weak_signals": "Schwache Signale",
        "avg_confidence": "Ø Vertrauensscore",
        "daily_recap": "Tägliche Zusammenfassung",
        "weekly_recap": "Wöchentliche Zusammenfassung",
        "scan_start": "🔍 *Starte automatische Analyse...*",
        "no_symbols_configured": "❌ Keine Symbole für die automatische Analyse konfiguriert.",
        "no_signals_found": "ℹ️ *Keine Handelssignale während der Analyse gefunden.*",
        "scan_complete_success": "✅ *Automatische Analyse erfolgreich abgeschlossen!*",
        "scan_complete_empty": "⚠️ *Analyse abgeschlossen – aber es wurden keine gültigen Signale generiert.*",
        "global_error_report": "⚠️ Unerwarteter Fehler aufgetreten:\n\n`{error}`",

        # === Notifications ===
        "notification_title": "Neues {action} Signal",
        "symbol": "Symbol",
        "move": "Kursbewegung",
        "volume_spike": "Volumenanstieg",
        "trend": "Trend",
        "confidence": "Vertrauen",
        "risk_reward": "Chance/Risiko",
        "notification_confidence_ultra": "⭐️ *Elite Setup* – Besser wird es nicht.",
        "notification_confidence_high": "🔍 *Starke Gelegenheit* – Bestätigt durch Trend & Volumen.",
        "notification_confidence_moderate": "⚠️ *Mittleres Setup* – Mit Vorsicht beobachten.",
        "notification_confidence_low": "❌ *Schwaches Signal* – Meiden oder nur beobachten.",
        "notification_footer": "_Handle mit Verstand. Kein FOMO – nur Präzision._"
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
