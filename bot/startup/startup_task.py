# bot/startup/startup_task.py

"""
A.R.K. Startup Task – Ultra Premium NASA Build 2025
Initialisiert alle Kernsysteme: ENV-Check, Systemzeitprüfung, Scheduler-Launch, Startup-Ping.
Maximale Stabilität für 24/7 Betrieb auf Koenigsegg-Niveau.
"""

import os
import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.scheduler.recap_scheduler import start_recap_scheduler
from bot.scheduler.heartbeat_job import start_heartbeat_job
from bot.scheduler.connection_watchdog_job import start_connection_watchdog
from bot.scheduler.news_scanner_job import news_scanner_job  # ✅ direkt asyncio loop

# === Logger & Settings Setup ===
logger = setup_logger(__name__)
settings = get_settings()

# === Core Startup Checks ===

def check_env_variables():
    required_vars = ["BOT_TOKEN", "TELEGRAM_CHAT_ID", "FINNHUB_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        logger.critical(f"❌ [Startup] Fehlende ENV-Variablen: {', '.join(missing)}")
        raise EnvironmentError(f"Fehlende ENV: {', '.join(missing)}")
    logger.info("✅ [Startup] ENV-Variablen erfolgreich geprüft.")

def check_system_time():
    utc_now = datetime.now(pytz.utc)
    if utc_now.year < 2023:
        logger.critical("❌ [Startup] Systemzeit ungültig.")
        raise ValueError("Systemzeit ist falsch eingestellt.")
    logger.info(f"✅ [Startup] Systemzeit korrekt: {utc_now.isoformat()}")

async def send_startup_ping(bot: Bot):
    try:
        await bot.send_message(
            chat_id=settings["TELEGRAM_CHAT_ID"],
            text="✅ *A.R.K. erfolgreich gestartet!*\n\n_Systems online. Ready to dominate._",
            parse_mode="Markdown"
        )
        logger.info("✅ [Startup] Startup-Ping erfolgreich gesendet.")
    except Exception as e:
        logger.error(f"❌ [Startup] Ping-Fehler: {e}")
        await report_error(bot, settings["TELEGRAM_CHAT_ID"], e, context_info="Startup Ping")

async def launch_background_jobs(application):
    bot = application.bot
    chat_id = int(settings["TELEGRAM_CHAT_ID"])

    # === Scheduler starten ===
    start_heartbeat_job(bot, chat_id)
    start_connection_watchdog(bot, chat_id)
    start_recap_scheduler(bot, chat_id)

    # === News Scanner starten (async Loop) ===
    asyncio.create_task(news_scanner_job())

    logger.info("✅ [Startup] Alle Scheduler erfolgreich aktiviert.")

async def execute_startup_tasks(application):
    logger.info("🚀 [Startup] Initialisiere A.R.K. Master-System...")

    try:
        check_env_variables()
        check_system_time()
        await launch_background_jobs(application)
        await send_startup_ping(application.bot)
        logger.info("✅ [Startup] A.R.K. vollständig einsatzbereit.")
    except Exception as e:
        logger.critical(f"🔥 [Startup] Initialisierungsfehler: {e}")
        raise
