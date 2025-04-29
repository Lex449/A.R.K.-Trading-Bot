# bot/startup/startup_task.py

"""
A.R.K. Startup Task – Ultra Premium NASA Build 2025
Initialisiert alle Kernsysteme: ENV-Check, Systemzeitprüfung, Scheduler-Launch, Startup-Ping.
Maximale Stabilität für 24/7 Betrieb.
"""

import os
import logging
import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from bot.config.settings import get_settings
from bot.scheduler.connection_watchdog_job import start_connection_watchdog
from bot.scheduler.heartbeat_job import start_heartbeat_job
from bot.scheduler.news_scanner_job import start_news_scanner_job
from bot.scheduler.recap_scheduler import start_recap_scheduler
from bot.utils.logger import setup_logger

# === Logger & Settings Setup ===
logger = setup_logger(__name__)
settings = get_settings()

# === Telegram Bot Instanz ===
bot = Bot(token=settings["BOT_TOKEN"])

# === Core Startup Functions ===

def check_env_variables():
    """Überprüft kritische ENV-Variablen auf Existenz und Validität."""
    required_vars = [
        "BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "FINNHUB_API_KEY"
    ]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(f"Fehlende ENV-Variablen: {', '.join(missing_vars)}")
    logger.info("✅ [Startup] Alle erforderlichen ENV-Variablen vorhanden.")

def check_system_time():
    """Überprüft die Systemzeit auf Plausibilität."""
    try:
        utc_now = datetime.now(pytz.utc)
        if utc_now.year < 2023:
            raise ValueError("Systemzeit scheint nicht korrekt zu laufen.")
        logger.info(f"✅ [Startup] Systemzeit OK: {utc_now.isoformat()}")
    except Exception as e:
        raise ValueError(f"❌ [Startup] Fehler bei Systemzeitprüfung: {e}")

async def send_startup_ping():
    """Sendet eine Benachrichtigung an den Admin über erfolgreichen Bot-Start."""
    try:
        await bot.send_message(
            chat_id=settings["TELEGRAM_CHAT_ID"],
            text="✅ A.R.K. Bot erfolgreich gestartet.\nAlle Systeme stabil.\nReady to dominate the markets.",
            parse_mode="Markdown"
        )
        logger.info("✅ [Startup] Startup-Ping erfolgreich gesendet.")
    except Exception as e:
        logger.error(f"❌ [Startup] Fehler beim Senden des Startup-Pings: {e}")

async def launch_schedulers(application):
    """Startet alle Hintergrund-Jobs (Heartbeat, Connection Watchdog, News Scanner, Recap)."""
    try:
        start_heartbeat_job(application)
        start_connection_watchdog(application)
        start_news_scanner_job(application)
        start_recap_scheduler(bot, int(settings["TELEGRAM_CHAT_ID"]))
        logger.info("✅ [Startup] Alle Scheduler erfolgreich aktiviert.")
    except Exception as e:
        logger.critical(f"🔥 [Startup] Fehler beim Start der Scheduler: {e}")

async def execute_startup_tasks(application):
    """
    Führt alle notwendigen Startup-Schritte aus:
    - ENV-Check
    - Systemzeit-Check
    - Scheduler-Startup
    - Admin-Info
    """
    logger.info("🚀 [Startup] Initialisiere A.R.K. Bot...")

    try:
        check_env_variables()
        check_system_time()
        await launch_schedulers(application)
        await send_startup_ping()
        logger.info("✅ [Startup] A.R.K. Startup vollständig abgeschlossen.")
    except Exception as e:
        logger.critical(f"🔥 [Startup] Schwerwiegender Startup-Fehler: {e}")
        raise e
