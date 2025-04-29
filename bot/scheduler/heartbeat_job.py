"""
A.R.K. Scheduler – Heartbeat Monitor 2025
Sends system health pings every 60 minutes to ensure uptime and transparency.
Made in Bali. Engineered with German Precision.
"""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import platform
import psutil
from telegram import Bot
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger

# Setup structured logger and settings
logger = setup_logger(__name__)
config = get_settings()

# Initialize global scheduler
heartbeat_scheduler = AsyncIOScheduler()

async def send_heartbeat(bot: Bot, chat_id: int):
    """
    Sends a structured heartbeat report via Telegram.

    Args:
        bot (Bot): Telegram bot instance.
        chat_id (int): Target chat ID.
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

        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"✅ [HeartbeatJob] Heartbeat sent to chat_id {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [HeartbeatJob] Failed to send heartbeat: {e}")

def start_heartbeat_job(bot: Bot, chat_id: int):
    """
    Starts the heartbeat job with 60-minute interval.

    Args:
        bot (Bot): Telegram bot instance.
        chat_id (int): Target chat ID.
    """
    try:
        heartbeat_scheduler.remove_all_jobs()

        heartbeat_scheduler.add_job(
            send_heartbeat,
            trigger=IntervalTrigger(minutes=60),
            args=[bot, chat_id],
            id=f"heartbeat_job_{chat_id}",
            replace_existing=True,
            name=f"A.R.K. Heartbeat Monitor for Chat {chat_id}",
            misfire_grace_time=300
        )

        if not heartbeat_scheduler.running:
            heartbeat_scheduler.start()

        logger.info(f"✅ [HeartbeatJob] Scheduler started for chat_id {chat_id}.")

    except Exception as e:
        logger.critical(f"🔥 [HeartbeatJob] Failed to start scheduler: {e}")
