import os
import logging
import time
from datetime import datetime
import pytz
from telegram import Bot

from bot.config.settings import get_settings

# Logger Setup
logger = logging.getLogger(__name__)
settings = get_settings()

# Telegram Bot Setup
bot = Bot(token=settings.telegram.bot_token)

def check_env_variables():
    """Überprüft kritische ENV-Variablen auf Existenz."""
    required_vars = [
        "TELEGRAM_BOT_TOKEN",
        "FINNHUB_API_KEY",
        "TWELVEDATA_API_KEY",
        "ADMIN_USER_ID"
    ]
    missing_vars = [var for var in required_vars if os.getenv(var) is None]
    if missing_vars:
        raise EnvironmentError(f"Fehlende ENV-Variablen: {', '.join(missing_vars)}")
    logger.info("Alle ENV-Variablen erfolgreich geprüft.")

def check_system_time():
    """Überprüft, ob die Systemzeit korrekt läuft."""
    try:
        utc_now = datetime.now(pytz.utc)
        if utc_now.year < 2023:
            raise ValueError("Systemzeit scheint nicht korrekt zu sein.")
        logger.info(f"Systemzeit-Check erfolgreich: {utc_now.isoformat()}")
    except Exception as e:
        raise ValueError(f"Fehler beim Systemzeit-Check: {e}")

def send_startup_ping():
    """Sendet eine Benachrichtigung an den Admin, dass der Bot erfolgreich läuft."""
    try:
        message = "✅ A.R.K. Bot gestartet.\n\nAlle Systeme stabil.\nReady to dominate the markets."
        bot.send_message(chat_id=settings.telegram.admin_user_id, text=message)
        logger.info("Startup-Ping erfolgreich an Admin gesendet.")
    except Exception as e:
        logger.error(f"Fehler beim Senden des Startup-Pings: {e}")

def startup_task():
    """Führt alle Startup-Prüfungen und -Benachrichtigungen aus."""
    logger.info("A.R.K. Bot Startup Task gestartet...")

    check_env_variables()
    check_system_time()
    send_startup_ping()

    logger.info("Startup Task abgeschlossen. A.R.K. ist bereit.")

# Platzhalter für spätere Erweiterungen
def autoupdate_check():
    """Optional: Autoupdate oder Version-Check."""
    pass
