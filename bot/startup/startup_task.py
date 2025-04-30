# bot/startup/startup_task.py

"""
A.R.K. Startup Task – Ultra Premium NASA Build 2025
Initialisiert alle Kernsysteme: ENV-Check, Systemzeitprüfung, Scheduler-Launch, Command-Menü, Startup-Ping.
Maximale Stabilität für 24/7 Betrieb auf Koenigsegg-Niveau.
"""

import os
import asyncio
from datetime import datetime
import pytz
from telegram import Bot, BotCommand
from bot.config.settings import get_settings
from bot.scheduler.connection_watchdog_job import start_connection_watchdog
from bot.scheduler.heartbeat_job import start_heartbeat_job
from bot.scheduler.news_scanner_job import start_news_scanner_job
from bot.scheduler.recap_scheduler import start_recap_scheduler
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text

# === Logger & Settings Setup ===
logger = setup_logger(__name__)
logger.propagate = False
settings = get_settings()


# === ENV-Check ===
def check_env_variables():
    required_vars = ["BOT_TOKEN", "TELEGRAM_CHAT_ID", "FINNHUB_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.critical(f"❌ [Startup] Fehlende ENV-Variablen: {', '.join(missing)}")
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")
    logger.info("✅ [Startup] Alle ENV-Variablen geladen.")


# === Zeitprüfung ===
def check_system_time():
    try:
        now = datetime.now(pytz.utc)
        if now.year < 2023:
            raise ValueError("Systemzeit inkorrekt.")
        logger.info(f"✅ [Startup] Systemzeit korrekt: {now.isoformat()}")
    except Exception as e:
        logger.critical(f"❌ [Startup] Zeitprüfung fehlgeschlagen: {e}")
        raise


# === BotCommand-Menü setzen ===
async def register_bot_commands(bot: Bot):
    try:
        commands = [
            BotCommand("start", "Start the bot"),
            BotCommand("help", "Show help & features"),
            BotCommand("analyse", "Analyse a stock"),
            BotCommand("signal", "Signal info"),
            BotCommand("status", "System status"),
            BotCommand("uptime", "Show uptime"),
            BotCommand("setlanguage", "Set your language"),
            BotCommand("shutdown", "Shutdown the bot"),
            BotCommand("monitor", "API usage overview")
        ]
        await bot.set_my_commands(commands)
        logger.info("✅ [Startup] Telegram Command-Menü gesetzt.")
    except Exception as e:
        logger.warning(f"⚠️ [Startup] Fehler beim Setzen der BotCommands: {e}")


# === Scheduler starten ===
async def launch_schedulers(application):
    try:
        bot = application.bot
        chat_id = int(settings["TELEGRAM_CHAT_ID"])

        start_heartbeat_job(bot, chat_id)
        start_connection_watchdog(bot, chat_id)
        start_news_scanner_job(bot, chat_id)
        start_recap_scheduler(bot, chat_id)

        logger.info("✅ [Startup] Alle Hintergrundjobs erfolgreich gestartet.")
    except Exception as e:
        logger.critical(f"🔥 [Startup] Scheduler-Start fehlgeschlagen: {e}")
        raise


# === Startup Notification ===
async def send_startup_ping(bot: Bot):
    try:
        lang = settings.get("BOT_LANGUAGE", "en")
        message = "✅ *A.R.K. erfolgreich gestartet!*\n\n_Systems online. Ready to dominate._"
        await bot.send_message(
            chat_id=settings["TELEGRAM_CHAT_ID"],
            text=message,
            parse_mode="Markdown"
        )
        logger.info("✅ [Startup] Startup-Benachrichtigung gesendet.")
    except Exception as e:
        logger.error(f"❌ [Startup] Fehler beim Senden der Startup-Nachricht: {e}")


# === MASTER-FUNKTION ===
async def execute_startup_tasks(application):
    """
    Führt alle Startup-Schritte in fester Reihenfolge aus:
    1. ENV-Validierung
    2. Zeitprüfung
    3. Command-Menü setzen
    4. Scheduler starten
    5. Admin-Benachrichtigung
    """
    logger.info("🚀 [Startup] A.R.K. Initialisierung startet...")

    try:
        check_env_variables()
        check_system_time()
        await register_bot_commands(application.bot)
        await launch_schedulers(application)
        await send_startup_ping(application.bot)
        logger.info("✅ [Startup] A.R.K. ist vollständig einsatzbereit.")
    except Exception as e:
        logger.critical(f"🔥 [Startup] Schwerwiegender Fehler beim Startup: {e}")
        raise
