"""
A.R.K. List Timezones Handler – Assists user timezone selection.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.timezone_manager import list_available_timezones
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def list_timezones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /listtimezones command.
    Lists available pytz timezones for user selection.
    """
    try:
        zones = list_available_timezones()
        message = "🌎 *Available Timezones:*\n\n" + "\n".join([f"`{zone}`" for zone in zones[:50]]) + "\n\n...and more."
        await update.message.reply_text(message, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error in /listtimezones: {e}")
        await update.message.reply_text("⚠️ Error loading timezone list.")
