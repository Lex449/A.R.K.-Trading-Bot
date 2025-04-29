# bot/auto/heartbeat_manager.py

"""
A.R.K. Heartbeat Manager – Ultra Stable Pulse System 2025.
Keeps the bot alive, sends regular heartbeats, detects downtime early.
"""

import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# === Logger Setup ===
logger = setup_logger(__name__)
config = get_settings()

# === Global Scheduler ===
heartbeat_scheduler = AsyncIOScheduler()

async def send_heartbeat(application, chat_id: int):
    """
    Sends a heartbeat message to Telegram every X minutes.
    Confirms that the bot is alive and operational.
    """
    try:
        await application.bot.send_message(
            chat_id=chat_id,
            text="✅ *Heartbeat:* A.R.K. Bot läuft stabil. Alle Systeme aktiv.",
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        logger.info(f"✅ [Heartbeat] Ping sent successfully to chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [Heartbeat] Failed to send heartbeat: {e}")

def start_heartbeat(application, chat_id: int, interval_minutes: int = 60):
    """
    Starts the Heartbeat scheduler with defined interval (default 60 minutes).
    """
    try:
        heartbeat_scheduler.remove_all_jobs()

        heartbeat_scheduler.add_job(
            send_heartbeat,
            trigger=IntervalTrigger(minutes=interval_minutes),
            args=[application, chat_id],
            id=f"heartbeat_ping_{chat_id}",
            replace_existing=True,
            name=f"Heartbeat Ping for Chat {chat_id}",
            misfire_grace_time=300  # 5 min tolerance if missed
        )

        if not heartbeat_scheduler.running:
            heartbeat_scheduler.start()

        logger.info(f"✅ [HeartbeatManager] Heartbeat Scheduler started every {interval_minutes} minutes for chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [HeartbeatManager] Failed to start Heartbeat Scheduler: {e}")
