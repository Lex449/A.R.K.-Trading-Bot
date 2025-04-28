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
    Handles the /status command.
    Provides live session metrics and trading activity overview.
    """
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name or "Trader"
    language = get_language(chat_id) or "en"

    try:
        logger.info(f"[Status] Command triggered by {user_name} (Chat ID: {chat_id})")

        # Retrieve Session Report
        session_summary = get_session_report()

        # Build Personalized Status Message
        message = (
            f"🔍 *Session Status – A.R.K. Trading Bot*\n\n"
            f"👤 *User:* `{user_name}`\n"
            f"📈 *Session Metrics:*\n\n"
            f"{session_summary}\n"
            f"_✅ System running ultra-stable. Powered by precision._"
        )

        # Send message with the session report
        await update.message.reply_text(message, parse_mode="Markdown")
        logger.info(f"[Status] Session report sent successfully.")

    except Exception as error:
        logger.error(f"[Status Handler Error] {error}")
        await report_error(context.bot, chat_id, error, context_info="Status Handler Failure")
