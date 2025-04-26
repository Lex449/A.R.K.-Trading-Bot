# bot/handlers/help.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.i18n import get_text
from bot.utils.language import get_language

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /help command.
    Provides the user with a list of available commands and descriptions.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        help_text = get_text("help", lang)
        await update.message.reply_text(help_text, parse_mode="Markdown")
        logger.info(f"[Help] {user} ({chat_id}) – Help command sent successfully.")
    except Exception as e:
        logger.error(f"[Help Error] {e}")
