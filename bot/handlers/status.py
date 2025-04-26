# bot/handlers/status.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.session_tracker import get_session_report
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /status command.
    Provides live session statistics: uptime, signal quality, performance metrics.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"
    lang = get_language(chat_id) or "en"

    try:
        logger.info(f"/status called by {user} (Chat ID: {chat_id})")

        # Sessiondaten abrufen
        summary_text = get_session_report()

        await update.message.reply_text(
            f"🔎 *Session Status for {user}:*\n\n{summary_text}",
            parse_mode="Markdown"
        )

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Status Handler Error")
        logger.error(f"Error during status command: {e}")
