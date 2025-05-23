"""
A.R.K. Startup Task – Ultra Premium NASA Build 2025.4  
Initialisiert alle Kernsysteme: ENV-Check, Systemzeitprüfung, Scheduler-Launch, Telegram-Ping.  
Made in Bali. Engineered with German Precision.
"""

import os
import asyncio
from datetime import datetime
import pytz
from telegram import Bot
from telegram.ext import Application, JobQueue

from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error
from bot.utils.language import get_language
from bot.utils.i18n import get_text

from bot.scheduler.recap_scheduler import start_recap_scheduler
from bot.scheduler.heartbeat_job import start_heartbeat_job
from bot.scheduler.connection_watchdog_job import start_connection_watchdog
from bot.scheduler.news_scanner_job import news_scanner_job
from bot.scheduler.auto_analysis_scheduler import start_auto_analysis_scheduler
from bot.auto.auto_signal_loop import auto_signal_loop

# === Logger & Settings ===
logger = setup_logger(__name__)
settings = get_settings()

def check_env_variables():
    required = ["BOT_TOKEN", "TELEGRAM_CHAT_ID", "FINNHUB_API_KEY"]
    missing = [var for var in required if not os.getenv(var)]
    if missing:
        logger.critical(f"❌ [Startup] Fehlende ENV-Variablen: {', '.join(missing)}")
        raise EnvironmentError(f"Fehlende ENV: {', '.join(missing)}")
    logger.info("✅ [Startup] ENV-Variablen erfolgreich geprüft.")

def check_system_time():
    utc_now = datetime.now(pytz.utc)
    if utc_now.year < 2023:
        logger.critical("❌ [Startup] Systemzeit ungültig.")
        raise ValueError("Systemzeit ist falsch eingestellt.")
    elif utc_now.year == 2023:
        logger.warning("⚠️ [Startup] Systemzeit wirkt veraltet – prüfen empfohlen.")
    logger.info(f"✅ [Startup] Systemzeit korrekt: {utc_now.isoformat()}")

async def send_startup_ping(bot: Bot):
    lang = get_language(settings["TELEGRAM_CHAT_ID"]) or "en"
    try:
        text = {
            "en": "✅ *A.R.K. successfully launched!*\n\nSystems online. Ready to dominate.",
            "de": "✅ *A.R.K. erfolgreich gestartet!*\n\nSysteme online. Bereit zur Dominanz."
        }.get(lang, "✅ *A.R.K. ready.*")

        menu = {
            "en": "\n\n*Quick Menu:* `/analyse`  `/signal`  `/status`  `/monitor`  `/help`",
            "de": "\n\n*Menü:* `/analyse`  `/signal`  `/status`  `/monitor`  `/help`"
        }.get(lang, "")

        await bot.send_message(
            chat_id=settings["TELEGRAM_CHAT_ID"],
            text=text + menu,
            parse_mode="Markdown"
        )
        logger.info("✅ [Startup] Telegram-Startmeldung gesendet.")
    except Exception as e:
        logger.error(f"❌ [Startup] Fehler beim Ping: {e}")
        await report_error(bot, settings["TELEGRAM_CHAT_ID"], e, context_info="Startup Ping")

async def launch_background_jobs(application: Application):
    bot = application.bot
    job_queue: JobQueue = application.job_queue
    chat_id = int(settings["TELEGRAM_CHAT_ID"])

    try:
        start_heartbeat_job(bot, chat_id)
        logger.info("✅ [Startup] Heartbeat aktiviert.")
    except Exception as e:
        logger.error(f"❌ Heartbeat Fehler: {e}")

    try:
        start_connection_watchdog(bot, chat_id)
        logger.info("✅ [Startup] Connection Watchdog aktiviert.")
    except Exception as e:
        logger.error(f"❌ Watchdog Fehler: {e}")

    try:
        start_recap_scheduler(bot, chat_id)
        logger.info("✅ [Startup] Recap Scheduler aktiviert.")
    except Exception as e:
        logger.error(f"❌ Recap Fehler: {e}")

    try:
        asyncio.create_task(news_scanner_job())
        logger.info("✅ [Startup] News Scanner aktiviert.")
    except Exception as e:
        logger.error(f"❌ News Scanner Fehler: {e}")

    try:
        asyncio.create_task(auto_signal_loop(application))
        logger.info("✅ [Startup] Auto Signal Loop gestartet.")
    except Exception as e:
        logger.error(f"❌ Auto Signal Loop Fehler: {e}")

    try:
        start_auto_analysis_scheduler(application)
        logger.info("✅ [Startup] Auto Analysis Scheduler gestartet.")
    except Exception as e:
        logger.error(f"❌ Auto Analysis Scheduler Fehler: {e}")

async def execute_startup_tasks(application: Application):
    logger.info("🚀 [Startup] Initialisiere A.R.K. Master-System...")
    try:
        check_env_variables()
        check_system_time()
        await launch_background_jobs(application)
        await send_startup_ping(application.bot)
        logger.info("✅ [Startup] System vollständig bereit.")
    except Exception as e:
        logger.critical(f"🔥 [Startup] Fehler beim Start: {e}")
        raise
