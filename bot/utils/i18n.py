# bot/utils/i18n.py

"""
A.R.K. i18n Engine – Ultra Premium Localization Framework 2025.
Handles bilingual support (English, German) for all bot messages.
"""

import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Translations (EN + DE) ===
translations = {
    "en": {
        "start": "👋 Hello {user}! Welcome to *A.R.K. Trading Bot 2.0*.\n\nUse /help to explore all commands!",
        "help": "ℹ️ *Available Commands:*\n/start – Start the bot\n/help – Command overview\n/analyse [symbol] – Analyze stock (e.g., /analyse AAPL)\n/signal – Get live signals\n/status – Session statistics\n/uptime – Show bot uptime\n/shutdown – Stop the bot\n/setlanguage [en/de] – Change language",
        "analysis_no_symbol": "❌ Please provide a symbol. Example: `/analyse AAPL`",
        "fetching_data_primary": "⏳ Fetching market data (Finnhub)...",
        "analysis_completed": "✅ Analysis completed!",
        "error_primary_source": "⚠️ Error fetching from Finnhub.",
        "set_language": "✅ Language changed successfully!",
        "shutdown": "🛑 Shutting down the bot. See you soon!",
        "global_error_report": "⚠️ Critical system error detected:\n```{error}```",
    },
    "de": {
        "start": "👋 Hallo {user}! Willkommen bei *A.R.K. Trading Bot 2.0*.\n\nNutze /help für alle Befehle!",
        "help": "ℹ️ *Verfügbare Befehle:*\n/start – Bot starten\n/help – Befehlsübersicht\n/analyse [Symbol] – Aktie analysieren (z.B. /analyse AAPL)\n/signal – Live-Signale erhalten\n/status – Session-Statistiken\n/uptime – Bot-Laufzeit anzeigen\n/shutdown – Bot stoppen\n/setlanguage [de/en] – Sprache ändern",
        "analysis_no_symbol": "❌ Bitte ein Symbol angeben. Beispiel: `/analyse AAPL`",
        "fetching_data_primary": "⏳ Marktdaten werden abgerufen (Finnhub)...",
        "analysis_completed": "✅ Analyse abgeschlossen!",
        "error_primary_source": "⚠️ Fehler beim Abrufen von Finnhub-Daten.",
        "set_language": "✅ Sprache erfolgreich geändert!",
        "shutdown": "🛑 Bot wird heruntergefahren. Bis bald!",
        "global_error_report": "⚠️ Kritischer Systemfehler erkannt:\n```{error}```",
    }
}

SUPPORTED_LANGUAGES = ["en", "de"]

def get_text(key: str, lang: str = "en") -> str:
    """
    Safely fetches the translation text for a given key and language.
    """
    try:
        if lang not in SUPPORTED_LANGUAGES:
            logger.warning(f"[i18n] Unsupported language: {lang}. Falling back to English.")
            lang = "en"

        return translations.get(lang, translations["en"]).get(key, f"⚠️ Missing translation for {key}")
    except Exception as e:
        logger.error(f"❌ [i18n Error] {e}")
        return f"⚠️ Error fetching translation for {key}"
