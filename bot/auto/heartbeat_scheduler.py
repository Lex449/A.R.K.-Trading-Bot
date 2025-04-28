# bot/auto/heartbeat_scheduler.py

"""
A.R.K. Heartbeat Scheduler – Live Pulse Monitoring
Sends automatic status pings to ensure bot uptime and transparency.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup Logger
logger = setup_logger(__name__)

# Global Heartbeat Scheduler
heartbeat_scheduler = AsyncIOScheduler()

def start_heartbeat(application):
    """
    Starts sending a heartbeat message at regular intervals (every 60 minutes).
    """
    config = get_settings()
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        # Sicherstellen, dass alte Jobs gelöscht sind
        heartbeat_scheduler.remove_all_jobs()

        # Alle 60 Minuten eine Ping-Nachricht
        heartbeat_scheduler.add_job(
            send_heartbeat,
            trigger=IntervalTrigger(minutes=60),
            args=[application, chat_id],
            id="heartbeat_ping",
            replace_existing=True,
            name="Heartbeat Ping"
        )

        if not heartbeat_scheduler.running:
            heartbeat_scheduler.start()

        logger.info("✅ [Heartbeat] Heartbeat Scheduler gestartet.")

    except Exception as e:
        logger.error(f"❌ [Heartbeat Error] Fehler beim Start des Heartbeats: {e}")

async def send_heartbeat(application, chat_id: int):
    """
    Sends a simple heartbeat message.
    """
    try:
        await application.bot.send_message(
            chat_id=chat_id,
            text="✅ *Heartbeat:* Bot läuft stabil. Alle Systeme aktiv.",
            parse_mode="Markdown"
        )
        logger.info(f"✅ [Heartbeat] Ping gesendet an Chat ID {chat_id}.")
    except Exception as e:
        logger.error(f"❌ [Heartbeat] Fehler beim Senden des Heartbeats: {e}")
