# bot/handlers/status.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.session_tracker import get_session_summary
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /status command.
    Provides a live session summary including total signals, quality, and uptime.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        # Fetch session summary
        summary_text = get_session_summary()

        # Send session summary
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🔎 *Session Status for {user}:*\n\n{summary_text}",
            parse_mode="Markdown"
        )

        logger.info(f"Status requested by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Status Command Error")
        logger.error(f"Error during status command: {e}")
