"""
A.R.K. Heartbeat Manager – Ultra Reliable Status Engine 2025
Sends real-time system pings with multilingual diagnostics and uptime clarity.
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

# Init Logger & Config
logger = setup_logger(__name__)
config = get_settings()

# Shared Scheduler
heartbeat_scheduler = AsyncIOScheduler()

def start_heartbeat_manager(application, chat_id: int):
    """
    Starts the heartbeat monitoring scheduler (every 60 minutes).
    """
    try:
        heartbeat_scheduler.remove_all_jobs()

        heartbeat_scheduler.add_job(
            send_heartbeat,
            trigger=IntervalTrigger(minutes=60),
            args=[application, chat_id],
            id=f"ultra_heartbeat_{chat_id}",
            name=f"A.R.K. Heartbeat Job for Chat {chat_id}",
            replace_existing=True,
            misfire_grace_time=300
        )

        if not heartbeat_scheduler.running:
            heartbeat_scheduler.start()

        logger.info(f"✅ [HeartbeatManager] Scheduler activated for chat_id {chat_id}.")

    except Exception as e:
        logger.critical(f"🔥 [HeartbeatManager] Failed to initialize: {e}")

async def send_heartbeat(application, chat_id: int):
    """
    Sends a multilingual heartbeat system status message.
    """
    try:
        lang = get_language(chat_id)

        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        system = platform.system()
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        message = (
            f"✅ *{get_text('heartbeat_title', lang)}*\n\n"
            f"*{get_text('status', lang)}:* `Stable`\n"
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

        logger.info(f"✅ [HeartbeatManager] Report dispatched to {chat_id}")

    except Exception as e:
        logger.error(f"❌ [HeartbeatManager] Failed to send report: {e}")
