"""
A.R.K. Scheduler – Heartbeat Monitor 2025.5
Sends multilingual system pings every 60 minutes to ensure uptime and diagnostics.
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
from bot.utils.language import get_language
from bot.utils.i18n import get_text

# Setup
logger = setup_logger(__name__)
config = get_settings()
heartbeat_scheduler = AsyncIOScheduler()

async def send_heartbeat(bot: Bot, chat_id: int):
    """
    Sends a structured heartbeat report via Telegram.
    """
    try:
        lang = get_language(chat_id) or "en"
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        system = platform.system()
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        status = get_text("status_stable", lang)
        if cpu > 85 or ram > 85:
            status = get_text("status_highload", lang)

        message = (
            f"✅ *{get_text('heartbeat_title', lang)}*\n\n"
            f"*{get_text('status', lang)}:* `{status}`\n"
            f"*{get_text('timestamp', lang)}:* `{now}`\n"
            f"*{get_text('cpu', lang)}:* `{cpu:.1f}%`\n"
            f"*{get_text('ram', lang)}:* `{ram:.1f}%`\n"
            f"*{get_text('system', lang)}:* `{system}`\n\n"
            f"_{get_text('heartbeat_footer', lang)}_"
        )

        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )
        logger.info(f"✅ [HeartbeatJob] Heartbeat sent to chat_id {chat_id}")

    except Exception as e:
        logger.error(f"❌ [HeartbeatJob] Failed to send heartbeat: {e}")

def start_heartbeat_job(bot: Bot, chat_id: int):
    """
    Starts the heartbeat job with 60-minute interval.
    """
    try:
        job_id = f"heartbeat_job_{chat_id}"

        # Prüfen ob Job bereits existiert
        if heartbeat_scheduler.get_job(job_id):
            logger.info(f"♻️ [HeartbeatJob] Scheduler already running for chat_id {chat_id}")
            return

        heartbeat_scheduler.add_job(
            send_heartbeat,
            trigger=IntervalTrigger(minutes=60),
            args=[bot, chat_id],
            id=job_id,
            name=f"A.R.K. Heartbeat for Chat {chat_id}",
            replace_existing=True,
            misfire_grace_time=300
        )

        if not heartbeat_scheduler.running:
            heartbeat_scheduler.start()

        logger.info(f"✅ [HeartbeatJob] Scheduler started for chat_id {chat_id}")

    except Exception as e:
        logger.critical(f"🔥 [HeartbeatJob] Failed to start scheduler: {e}")
