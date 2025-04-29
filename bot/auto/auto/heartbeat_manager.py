# bot/auto/heartbeat_manager.py

"""
A.R.K. Heartbeat Manager – Ultra Reliable Status Engine
Sends real-time system health pings to ensure uptime & transparency.
"""

from datetime import datetime
import logging
import platform
import psutil
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

# Global Scheduler
heartbeat_scheduler = AsyncIOScheduler()

def start_heartbeat_manager(application, chat_id: int):
    """
    Initializes the heartbeat job that runs every 60 minutes.
    """
    try:
        heartbeat_scheduler.remove_all_jobs()

        heartbeat_scheduler.add_job(
            send_heartbeat,
            trigger=IntervalTrigger(minutes=60),
            args=[application, chat_id],
            id=f"ultra_heartbeat_{chat_id}",
            replace_existing=True,
            name=f"A.R.K. Heartbeat Manager for Chat {chat_id}",
            misfire_grace_time=300
        )

        if not heartbeat_scheduler.running:
            heartbeat_scheduler.start()

        logger.info(f"✅ [HeartbeatManager] Scheduler started for chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [HeartbeatManager] Failed to start: {e}")

async def send_heartbeat(application, chat_id: int):
    """
    Sends a structured system heartbeat report.
    """
    try:
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        system = platform.system()
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        message = (
            "✅ *A.R.K. Heartbeat Report*\n\n"
            f"*Status:* Stable\n"
            f"*Time:* `{timestamp}`\n"
            f"*CPU Usage:* `{cpu:.1f}%`\n"
            f"*RAM Usage:* `{ram:.1f}%`\n"
            f"*System:* `{system}`\n"
            "_A.R.K. is watching the markets._"
        )

        await application.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        logger.info(f"✅ [HeartbeatManager] Heartbeat sent to {chat_id}")

    except Exception as e:
        logger.error(f"❌ [HeartbeatManager] Failed to send heartbeat: {e}")
