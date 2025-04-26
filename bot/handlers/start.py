# bot/handlers/start.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error

# Setup Logger
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /start command.
    Greets the user and provides help instructions.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        lang = get_language(update)
        greeting = get_text("start", lang).format(user=user)
        help_text = get_text("help", lang)

        await update.message.reply_text(f"{greeting}\n\n{help_text}")

        logger.info(f"[START] {user} (Chat ID: {chat_id}) initiated /start.")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Start Command Error")
        logger.error(f"[START ERROR] {e}")
