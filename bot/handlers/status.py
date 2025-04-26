# bot/handlers/status.py

from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.session_tracker import get_session_report
from bot.utils.logger import setup_logger
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /status command.
    Returns live statistics about the current trading session.
    """
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name or "Trader"

    logger.info(f"Status requested by {user} (Chat ID: {chat_id})")

    try:
        session_summary = get_session_report()

        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🔎 *Session Status for {user}:*\n\n{session_summary}",
            parse_mode="Markdown"
        )

        logger.info(f"Session status sent successfully to {user}.")

    except Exception as e:
        await report_error(context.bot, chat_id, e, context_info="Status Handler Error")
        logger.error(f"Error during /status command execution: {e}")
