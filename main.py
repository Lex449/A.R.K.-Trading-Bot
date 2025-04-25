import os
import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters

# Laden der Umgebungsvariablen aus .env-Datei
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN is not set in the environment variables")

# Logging-Konfiguration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Import der Handler-Funktionen
from bot.handlers.commands import start, help_command, analyse_symbol, set_language
from bot.auto.auto_analysis import run_auto_analysis

def main():
    """Hauptfunktion zum Starten des Telegram-Bots."""
    # Bot-Anwendung initialisieren
    application = ApplicationBuilder().token(TOKEN).build()

    # Command-Handler registrieren
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("analyse", analyse_symbol))
    application.add_handler(CommandHandler("setlanguage", set_language))

    # Automatische Analyse (täglich) einrichten, falls ADMIN_CHAT_ID gesetzt
    admin_chat_id = os.getenv("ADMIN_CHAT_ID")
    if admin_chat_id:
        from datetime import time
        admin_chat_id = int(admin_chat_id)
        # Beispiel: Täglich um 14:00 UTC
        application.job_queue.run_daily(
            callback=run_auto_analysis,
            time=time(hour=14, minute=0),
            days=(0,1,2,3,4,5,6),
            context=admin_chat_id
        )
        logger.info("Automatische tägliche Analyse aktiviert für Chat ID %s", admin_chat_id)

    # Bot starten (Polling)
    logger.info("Starte Bot (Polling-Modus)")
    application.run_polling()

if __name__ == "__main__":
    main()