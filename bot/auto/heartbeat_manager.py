# bot/auto/heartbeat_manager.py

"""
A.R.K. Heartbeat Manager – Pulse Alive System.
Sends heartbeats to confirm the bot is alive.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

heartbeat_scheduler = AsyncIOScheduler()

def start_heartbeat_manager(application, chat_id: int):
    """
    Starts the heartbeat scheduler at startup.
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

        logger.info(f"✅ [HeartbeatManager] Heartbeat Scheduler started for chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [HeartbeatManager] Failed to start Heartbeat Manager: {e}")

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
        logger.error(f"❌ [Heartbeat] Failed to send heartbeat: {e}")
