"""
A.R.K. Start Command – Ultra Structured Premium Build.
Welcomes user, sets first interaction experience.
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
        # Load text templates
        greeting_text = get_text("start_greeting", language).format(user=user_name)
        help_hint_text = get_text("start_help_hint", language)

        # Send welcome message
        await update.message.reply_text(
            f"{greeting_text}\n\n{help_hint_text}",
            parse_mode="Markdown"
        )

        logger.info(f"/start command triggered | User: {user_name} | Chat ID: {chat_id}")

    except Exception as error:
        await report_error(context.bot, chat_id, error, context_info="/start command failure")
        logger.error(f"/start command error: {error}")
