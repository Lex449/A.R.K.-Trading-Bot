# bot/handlers/start.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.i18n import get_text
from bot.utils.language import get_language

# Setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /start command.
    Sends a welcome message and basic bot information.
    """
    user = update.effective_user.first_name or "Trader"
    chat_id = update.effective_chat.id
    lang = get_language(chat_id) or "en"

    greeting = get_text("start", lang).format(user=user)
    help_text = get_text("help", lang)

    try:
        await update.message.reply_text(f"{greeting}\n\n{help_text}", parse_mode="Markdown")
        logger.info(f"[Start] {user} ({chat_id}) – Start command received.")
    except Exception as e:
        logger.error(f"[Start Error] {e}")
