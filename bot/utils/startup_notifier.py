"""
A.R.K. Startup Notifier – Ultra Professional Boot Message.
Sends clean, human-grade startup confirmation to Telegram.
"""

import logging
from datetime import datetime
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.config.settings import get_settings
from telegram import Bot

# Setup Logger
logger = setup_logger(__name__)
config = get_settings()

async def send_startup_notification(bot: Bot, chat_id: int):
    """
    Sends a one-time startup notification to the bot admin.
    """
    try:
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        lang = get_language(chat_id) or "en"

        header = "🚀 *A.R.K. Bot Started*" if lang == "en" else "🚀 *A.R.K. Bot Gestartet*"
        environment = config.get("ENVIRONMENT", "Production")
        body = (
            f"*Environment:* `{environment}`\n"
            f"*Time:* `{now}`\n"
            f"*Heartbeat:* Active\n"
            f"*Auto Signal:* Active\n"
            f"*Market Monitoring:* Active\n\n"
            "_Made in Bali. Engineered with German Precision._"
        )

        message = f"{header}\n\n{body}"

        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"✅ [StartupNotifier] Startup message sent to Chat ID: {chat_id}")

    except Exception as e:
        logger.error(f"❌ [StartupNotifier] Failed to send startup message: {e}")
