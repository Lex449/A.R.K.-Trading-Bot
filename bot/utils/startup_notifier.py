"""
A.R.K. Startup Notifier – Ultra Professional Boot Message.
Sends clean, human-grade startup confirmation to Telegram.
Made in Bali. Engineered with German Precision.
"""

from datetime import datetime
from telegram import Bot
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.config.settings import get_settings

# Setup Logger & Config
logger = setup_logger(__name__)
config = get_settings()

async def send_startup_notification(bot: Bot, chat_id: int) -> None:
    """
    Sends a multilingual startup notification to the administrator.

    Args:
        bot (Bot): Telegram Bot instance.
        chat_id (int): Telegram chat ID.
    """
    try:
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
        lang = get_language(chat_id) or "en"
        env = config.get("ENVIRONMENT", "Production")

        header = get_text("startup_title", lang)
        body = (
            f"*{get_text('startup_env', lang)}:* `{env}`\n"
            f"*{get_text('startup_time', lang)}:* `{now}`\n"
            f"*{get_text('startup_heartbeat', lang)}:* ✅\n"
            f"*{get_text('startup_autosignal', lang)}:* ✅\n"
            f"*{get_text('startup_marketwatch', lang)}:* ✅\n\n"
            f"_{get_text('startup_footer', lang)}_"
        )

        message = f"{header}\n\n{body}"

        await bot.send_message(
            chat_id=chat_id,
            text=message,
            parse_mode="Markdown",
            disable_web_page_preview=True
        )

        logger.info(f"✅ [StartupNotifier] Startup message sent to chat ID {chat_id}.")

    except Exception as e:
        logger.error(f"❌ [StartupNotifier] Failed to send startup message: {e}")
