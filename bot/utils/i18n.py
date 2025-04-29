"""
A.R.K. Internationalization (i18n) Engine – Ultra Premium Localization Build.
Handles multilingual support for all bot interactions.
"""

import logging
from bot.utils.logger import setup_logger

# Setup Structured Logger
logger = setup_logger(__name__)

# === Supported Translations ===
translations = {
    "en": {
        "start": "👋 Hello {user}! Welcome to *A.R.K. Trading Bot*.\n\nUse /help to explore available features.",
        "help": "ℹ️ *Available Commands:*\n/start – Start the bot\n/help – Show commands\n/analyse [symbol] – Analyze a symbol (e.g., /analyse AAPL)\n/signal – Live signals\n/status – Current bot statistics\n/uptime – Bot running time\n/shutdown – Shut down bot",
        "analysis_no_symbol": "❌ Please provide a valid symbol. Example: `/analyse AAPL`",
        "signal_sent": "✅ Signal sent successfully!",
        "signal_failed": "❌ Signal could not be sent.",
        "session_summary": "📊 *Session Summary*",
        "uptime": "⏱️ *Bot Uptime:*",
        "shutdown": "🛑 Bot is shutting down. See you soon!",
        "language_changed": "✅ Language updated successfully!",
        "error_occurred": "❌ An unexpected error occurred. Please try again later.",
        "health_ok": "✅ *System Health Check:* All systems operational.",
        "health_fail": "❌ *System Health Check:* Failure detected.",
        "global_error_report": "⚠️ An unexpected error occurred:\n\n`{error}`",
    },
    "de": {
        "start": "👋 Hallo {user}! Willkommen beim *A.R.K. Trading Bot*.\n\nVerwende /help, um verfügbare Funktionen zu entdecken.",
        "help": "ℹ️ *Verfügbare Befehle:*\n/start – Bot starten\n/help – Befehle anzeigen\n/analyse [Symbol] – Symbol analysieren (z.B. /analyse AAPL)\n/signal – Live-Signale\n/status – Aktuelle Bot-Statistik\n/uptime – Laufzeit des Bots\n/shutdown – Bot herunterfahren",
        "analysis_no_symbol": "❌ Bitte ein gültiges Symbol angeben. Beispiel: `/analyse AAPL`",
        "signal_sent": "✅ Signal erfolgreich gesendet!",
        "signal_failed": "❌ Signal konnte nicht gesendet werden.",
        "session_summary": "📊 *Session Zusammenfassung*",
        "uptime": "⏱️ *Bot Laufzeit:*",
        "shutdown": "🛑 Bot wird heruntergefahren. Bis bald!",
        "language_changed": "✅ Sprache erfolgreich geändert!",
        "error_occurred": "❌ Ein unerwarteter Fehler ist aufgetreten. Bitte später erneut versuchen.",
        "health_ok": "✅ *System Gesundheitscheck:* Alle Systeme betriebsbereit.",
        "health_fail": "❌ *System Gesundheitscheck:* Fehler erkannt.",
        "global_error_report": "⚠️ Ein unerwarteter Fehler ist aufgetreten:\n\n`{error}`",
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
        str: Translated string, or fallback if missing.
    """
    try:
        if lang not in SUPPORTED_LANGUAGES:
            logger.warning(f"[i18n] Unsupported language '{lang}', defaulting to English.")
            lang = "en"

        lang_data = translations.get(lang, translations["en"])
        text = lang_data.get(key)

        if text:
            return text
        else:
            logger.warning(f"[i18n] Missing translation key '{key}' for language '{lang}'.")
            return f"🔍 Missing translation for `{key}`"

    except Exception as e:
        logger.error(f"[i18n] Fatal translation lookup error: {e}")
        return f"⚠️ Translation Error for `{key}`"
