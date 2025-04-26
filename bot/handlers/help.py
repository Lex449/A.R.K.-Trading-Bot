# bot/handlers/help.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.utils.error_reporter import report_error

# Setup Logger
logger = logging.getLogger(__name__)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /help command.
    Provides an overview of all available bot commands.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        lang = get_language(update)
        help_text = get_text("help", lang)

        await update.message.reply_text(help_text)

        logger.info(f"[HELP] Help command requested by {user} (Chat ID: {chat_id}).")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Help Command Error")
        logger.error(f"[HELP ERROR] {e}")
