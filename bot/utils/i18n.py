# bot/utils/i18n.py

"""
Internationalization (i18n) module.
Handles multilingual text output for user interaction.
"""

import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Translation mappings
translations = {
    "en": {
        "start": "👋 Hello {user}! Welcome to *A.R.K. Trading Bot 2.0*.\n\nUse /help to view available commands and start trading smarter.",
        "help": "ℹ️ *Available Commands:*\n\n/start – Start the bot\n/help – Command overview\n/analyse [symbol] – Analyze a symbol (e.g., /analyse AAPL)\n/setlanguage [en/de] – Change language\n/signal – Get current trading signals\n/status – Show session statistics\n/shutdown – Stop the bot",
        "analysis_no_symbol": "❌ Please provide a valid symbol. Example: `/analyse AAPL`",
        "set_language": "✅ Language updated successfully. All future messages will be sent in your selected language.",
        "shutdown": "🛑 Bot is shutting down. Stay tuned for the next session!",
    },
    "de": {
        "start": "👋 Hallo {user}! Willkommen bei *A.R.K. Trading Bot 2.0*.\n\nNutze /help, um alle verfügbaren Befehle anzuzeigen und smarter zu traden.",
        "help": "ℹ️ *Verfügbare Befehle:*\n\n/start – Bot starten\n/help – Befehlsübersicht\n/analyse [Symbol] – Ein Symbol analysieren (z.B. /analyse AAPL)\n/setlanguage [de/en] – Sprache ändern\n/signal – Aktuelle Handelssignale abrufen\n/status – Session-Statistik anzeigen\n/shutdown – Bot stoppen",
        "analysis_no_symbol": "❌ Bitte gib ein gültiges Symbol an. Beispiel: `/analyse AAPL`",
        "set_language": "✅ Sprache erfolgreich aktualisiert. Alle weiteren Nachrichten folgen in der gewählten Sprache.",
        "shutdown": "🛑 Der Bot wird beendet. Bis zum nächsten Einsatz!",
    }
}

def get_text(key: str, lang: str = "en") -> str:
    """
    Returns the localized text for a given key and language.
    
    Args:
        key (str): The text identifier key.
        lang (str): Language code ('en', 'de').

    Returns:
        str: The translated text, or a fallback if key is missing.
    """
    try:
        lang_data = translations.get(lang, translations["en"])
        return lang_data.get(key, f"🔍 Unknown text key: `{key}`")
    except Exception as e:
        logger.error(f"i18n lookup error: {e}")
        return f"🔍 Translation error for key: `{key}`"
