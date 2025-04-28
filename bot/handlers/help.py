"""
A.R.K. Help Command – Bilingual Ultra Build.
Provides users with a clean overview of all available commands.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /help command.
    Sends an ultra-clean command overview, bilingual, Markdown-optimized.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"  # Get language based on chat ID, fallback to English

    try:
        # Load the help text based on user language
        help_text = get_text("help_overview", lang)

        # Send the formatted help message to the user
        await update.message.reply_text(
            help_text,
            parse_mode="Markdown"  # Using Markdown for clean formatting
        )

        # Log the usage of the help command with the user's language
        logger.info(f"[Help] Triggered by {user} ({lang})")

    except Exception as e:
        # If an error occurs, report it and log the error
        await report_error(context.bot, chat_id, e, context_info="Help Command Error")
        logger.error(f"[Help Error] {e}")
