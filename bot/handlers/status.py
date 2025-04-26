import logging
from telegram import Update
from telegram.ext import ContextTypes
from bot.utils.session_tracker import get_session_report
from bot.utils.language import get_language
from bot.utils.i18n import get_text
from bot.utils.error_reporter import report_error

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def status_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handler for /status command.
    Provides a live overview of the current trading session.
    """
    chat_id = update.effective_chat.id

    try:
        session_report = get_session_report()

        message = (
            f"✅ *A.R.K. Bot Status Report*\n\n"
            f"{session_report}\n\n"
            f"📡 _Data updated live._"
        )

        await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        logger.info(f"Status report sent to {update.effective_user.first_name}")

    except Exception as e:
        logger.error(f"[Status Error] Failed to retrieve session report: {e}")
        await report_error(context.bot, chat_id, e, context_info="Status Handler Error")
