"""
A.R.K. Start Command – Ultra Structured Premium Build.
Welcomes the user with precision and motivation.
"""

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles the /start command.
    Provides a localized, structured welcome message.
    """
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or "Trader"
    language = get_language(chat_id) or "en"

    try:
        # Load localized welcome and help texts
        greeting = get_text("start_greeting", language).format(user=user_name)
        help_hint = get_text("start_help_hint", language)

        # Compose full welcome message
        welcome_message = (
            f"{greeting}\n\n"
            f"{help_hint}\n\n"
            f"🚀 _Precision. Discipline. Execution._"
        )

        # Send welcome message to the user
        await update.message.reply_text(
            welcome_message,
            parse_mode="Markdown"
        )

        # Log user session start
        logger.info(f"[Start] User '{user_name}' initialized session (Chat ID: {chat_id})")

    except Exception as error:
        # Log error if occurs and send error report
        logger.error(f"[Start Command Error] {error}")
        await report_error(context.bot, chat_id, error, context_info="Start Command Failure")
