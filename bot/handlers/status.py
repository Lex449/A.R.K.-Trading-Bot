# bot/handlers/status.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.session_tracker import get_session_report
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger
from bot.config.settings import get_settings

# Setup structured logger
logger = setup_logger(__name__)

# Load configuration
config = get_settings()

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /status command.
    Provides live session overview with uptime, signals, and quality stats.
    """
    user = update.effective_user.first_name or "Trader"
    chat_id = update.effective_chat.id

    logger.info(f"/status command triggered by {user} (Chat ID: {chat_id})")

    try:
        session_report = get_session_report()

        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🔎 *Session Status for {user}:*\n\n{session_report}",
            parse_mode="Markdown"
        )

        logger.info(f"Session status sent to {user}")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Status Command Error")
        logger.error(f"Error during status command: {e}")
