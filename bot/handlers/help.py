# bot/handlers/help.py

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
    Handler for /help command.
    Sends a detailed list of available commands and their usage.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        help_text = get_text("help_overview", lang)

        await update.message.reply_text(
            help_text,
            parse_mode="Markdown"
        )

        logger.info(f"Help command triggered by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Help Command Error")
        logger.error(f"Error in /help command: {e}")
