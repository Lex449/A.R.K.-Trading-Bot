"""
A.R.K. Heartbeat Scheduler – Hyper Precision Live Monitoring
Sends dynamic status pings to ensure bot uptime, transparency, and system health.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings
from bot.utils.market_time import is_trading_day, is_trading_hours

# Setup Logger
logger = setup_logger(__name__)

# Global Scheduler Instance
heartbeat_scheduler = AsyncIOScheduler()

def start_heartbeat(application):
    """
    Initializes the heartbeat scheduler with live status updates every 60 minutes.
    """
    config = get_settings()
    chat_id = int(config["TELEGRAM_CHAT_ID"])

    try:
        # Remove all previous jobs to prevent duplicates
        heartbeat_scheduler.remove_all_jobs()

        # Schedule Heartbeat every 60 minutes
        heartbeat_scheduler.add_job(
            send_heartbeat,
            trigger=IntervalTrigger(minutes=60),
            args=[application, chat_id],
            id="heartbeat_ping",
            replace_existing=True,
            name="Heartbeat Ping Job"
        )

        if not heartbeat_scheduler.running:
            heartbeat_scheduler.start()

        logger.info("✅ [Heartbeat] Heartbeat Scheduler launched successfully.")

    except Exception as e:
        logger.error(f"❌ [Heartbeat Error] Failed to start scheduler: {e}")

async def send_heartbeat(application, chat_id: int):
    """
    Sends a heartbeat message indicating system health and market status.
    """
    try:
        # Dynamische Statusanzeige je nach Marktzustand
        if is_trading_day():
            if is_trading_hours():
                status_text = "✅ *Heartbeat:* System stabil. Märkte sind OFFEN."
            else:
                status_text = "✅ *Heartbeat:* System stabil. Märkte aktuell GESCHLOSSEN."
        else:
            status_text = "✅ *Heartbeat:* System stabil. Heute kein Handelstag."

        await application.bot.send_message(
            chat_id=chat_id,
            text=status_text,
            parse_mode="Markdown"
        )
        logger.info(f"✅ [Heartbeat] Status-Ping gesendet an Chat ID {chat_id}: {status_text}")

    except Exception as e:
        logger.error(f"❌ [Heartbeat] Fehler beim Senden des Heartbeats: {e}")
