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

def start_heartbeat(application, chat_id: int):
    """
    Starts sending a heartbeat message at regular intervals (every 60 minutes).
    """
    try:
        heartbeat_scheduler.remove_all_jobs()

        heartbeat_scheduler.add_job(
            send_heartbeat,
            trigger=IntervalTrigger(minutes=60),
            args=[application, chat_id],
            id=f"heartbeat_ping_{chat_id}",
            replace_existing=True,
            name=f"Heartbeat Ping for Chat {chat_id}"
        )

        if not heartbeat_scheduler.running:
            heartbeat_scheduler.start()

        logger.info(f"✅ [Heartbeat] Heartbeat Scheduler started for chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [Heartbeat Error] Failed to start heartbeat scheduler: {e}")

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
        logger.info(f"✅ [Heartbeat] Ping sent to chat_id {chat_id}.")
    except Exception as e:
        logger.error(f"❌ [Heartbeat] Failed to send heartbeat to chat_id {chat_id}: {e}")
