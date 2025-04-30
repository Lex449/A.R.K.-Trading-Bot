"""
A.R.K. Heartbeat Manager – Ultra Reliable Status Engine 2025+
Sends real-time system pings with multilingual diagnostics, resource checks and uptime clarity.
Made in Bali. Engineered with German Precision.
"""

from datetime import datetime
import platform
import psutil
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bot.utils.logger import setup_logger
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.config.settings import get_settings

# Logger & Config
logger = setup_logger(__name__)
config = get_settings()

# Singleton Scheduler Instance
heartbeat_scheduler = AsyncIOScheduler()

def start_heartbeat_manager(application, chat_id: int):
    """
    Starts the heartbeat scheduler that pings status every 60 minutes.
    """
    try:
        if heartbeat_scheduler.get_job(f"ultra_heartbeat_{chat_id}"):
            logger.info(f"♻️ [HeartbeatManager] Scheduler already running for chat_id {chat_id}")
            return

        heartbeat_scheduler.add_job(
            send_heartbeat,
            trigger=IntervalTrigger(minutes=60),
            args=[application, chat_id],
            id=f"ultra_heartbeat_{chat_id}",
            name=f"A.R.K. Heartbeat for {chat_id}",
            replace_existing=True,
            misfire_grace_time=300
        )

        if not heartbeat_scheduler.running:
            heartbeat_scheduler.start()

        logger.info(f"✅ [HeartbeatManager] Scheduler started for chat_id {chat_id}")

    except Exception as e:
        logger.critical(f"🔥 [HeartbeatManager] Failed to initialize: {e}")

async def send_heartbeat(application, chat_id: int):
    """
    Sends detailed diagnostic report to Telegram.
    """
    try:
        lang = get_language(chat_id)
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        system = platform.system()
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        status_note = "✅ Stable"
        if cpu >= 85 or ram >= 85:
            status_note = "⚠️ High Load"

        message = (
            f"✅ *{get_text('heartbeat_title', lang)}*\n\n"
            f"*{get_text('status', lang)}:* `{status_note}`\n"
            f"*{get_text('timestamp', lang)}:* `{now}`\n"
            f"*{get_text('cpu', lang)}:* `{cpu:.1f}%`\n"
            f"*{get_text('ram', lang)}:* `{ram:.1f}%`\n"
            f"*{get_text('system', lang)}:* `{system}`\n\n"
            f"_{get_text('heartbeat_footer', lang)}_"
        )

        await application.bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"✅ [HeartbeatManager] Status sent to {chat_id}")

    except Exception as e:
        logger.exception(f"❌ [HeartbeatManager] Could not send heartbeat to {chat_id}: {e}")
