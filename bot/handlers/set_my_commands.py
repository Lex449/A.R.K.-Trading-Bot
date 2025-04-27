"""
A.R.K. Command List Setter – Ultra Premium Build.
Defines a crystal-clear command set for Telegram with bilingual readiness.
"""

from telegram import BotCommand
from bot.utils.language import get_language

async def set_bot_commands(application):
    """
    Dynamically sets the bot's command list based on user language preference.
    """

    # Default language fallback
    lang = "en"

    try:
        # If possible, pull admin chat language
        chat_id = application.bot.id  # fallback fallback fallback
        lang = get_language(chat_id) or "en"
    except Exception:
        pass  # silently continue with English

    if lang == "de":
        commands = [
            BotCommand("start", "Starte den Bot"),
            BotCommand("help", "Zeige Hilfe und Befehle"),
            BotCommand("analyse", "Analysiere ein Symbol (/analyse AAPL)"),
            BotCommand("signal", "Hole aktuelle Handelssignale"),
            BotCommand("status", "Zeige Sitzungsstatistiken"),
            BotCommand("shutdown", "Bot stoppen"),
            BotCommand("testsignal", "Test-Signal senden"),
            BotCommand("testanalyse", "Test-Analyse senden"),
            BotCommand("ping", "Überprüfe Reaktionszeit"),
            BotCommand("health", "Systemzustand prüfen"),
        ]
    else:
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Show help and command list"),
            BotCommand("analyse", "Analyse a symbol (e.g. /analyse AAPL)"),
            BotCommand("signal", "Get current trading signals"),
            BotCommand("status", "Show session statistics"),
            BotCommand("shutdown", "Stop the bot"),
            BotCommand("testsignal", "Send a test trading signal"),
            BotCommand("testanalyse", "Send a test symbol analysis"),
            BotCommand("ping", "Check bot response time"),
            BotCommand("health", "Check system health"),
        ]

    await application.bot.set_my_commands(commands)
