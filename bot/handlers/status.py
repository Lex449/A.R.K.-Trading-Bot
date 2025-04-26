# bot/handlers/status.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.session_tracker import get_session_report
from bot.utils.error_reporter import report_error

# Setup Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /status command.
    Provides a real-time summary of the bot's session performance.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    try:
        # Session-Daten holen
        session_text = get_session_report()

        await context.bot.send_message(
            chat_id=chat_id,
            text=f"📊 *Session Status for {user}:*\n\n{session_text}",
            parse_mode="Markdown"
        )

        logger.info(f"✅ Status command requested successfully by {user} (Chat ID: {chat_id})")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Status Command Error")
        logger.error(f"❌ Error in /status triggered by {user}: {e}")
