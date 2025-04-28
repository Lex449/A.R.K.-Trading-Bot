"""
A.R.K. List Timezones Handler – Assists user timezone selection.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.timezone_manager import list_available_timezones
from bot.utils.i18n import get_text
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def list_timezones(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles /listtimezones command.
    Lists available pytz timezones for user selection.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_text("language", chat_id) or "en"

    try:
        # Fetch all available timezones
        zones = list_available_timezones()

        # Split zones into manageable chunks if too long
        if len(zones) > 50:
            message = "🌎 *Available Timezones:*\n\n" + "\n".join([f"`{zone}`" for zone in zones[:50]]) + "\n\n...and more."
        else:
            message = "🌎 *Available Timezones:*\n\n" + "\n".join([f"`{zone}`" for zone in zones])

        # Send timezones in a single message
        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"/listtimezones used by {user} (Chat ID: {chat_id})")

    except Exception as e:
        logger.error(f"Error in /listtimezones: {e}")
        await update.message.reply_text(
            get_text("error_loading_timezones", lang),
            parse_mode="Markdown"
        )
        raise  # Reraise the error to be caught by global error handler
