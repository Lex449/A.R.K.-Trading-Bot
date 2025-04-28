"""
A.R.K. Bot Commands Setter – Strategic Command Management.
Dynamically adjusts the command list based on language preference.
"""

from telegram import BotCommand
from bot.utils.language import get_language
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def set_bot_commands(application):
    """
    Dynamically sets the bot's command list based on user's or admin's language preference.
    Clean fallback logic for maximum resilience.
    """
    lang = "en"  # Default language

    try:
        # Attempt to get preferred language
        chat_id = application.bot.id  # Bot ID fallback
        lang = get_language(chat_id) or "en"
    except Exception as e:
        logger.warning(f"[SetBotCommands] Could not detect language, using default EN. ({e})")

    # === Define Commands ===
    commands = []

    if lang == "de":
        commands = [
            BotCommand("start", "Starte den Bot"),
            BotCommand("help", "Zeige Hilfe und Befehle"),
            BotCommand("analyse", "Analysiere ein Symbol (z.B. /analyse AAPL)"),
            BotCommand("signal", "Hole aktuelle Handelssignale"),
            BotCommand("status", "Zeige Sitzungsstatistiken"),
            BotCommand("shutdown", "Bot beenden"),
            BotCommand("testsignal", "Test-Handelssignal senden"),
            BotCommand("testanalyse", "Test-Analyse ausführen"),
            BotCommand("ping", "Antwortzeit prüfen"),
            BotCommand("health", "Systemgesundheit prüfen"),
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

    try:
        # Set commands at Telegram level
        await application.bot.set_my_commands(commands)
        logger.info(f"✅ [SetBotCommands] Commands successfully updated (Language: {lang}).")
    except Exception as e:
        logger.error(f"❌ [SetBotCommands] Failed to update commands: {e}")
