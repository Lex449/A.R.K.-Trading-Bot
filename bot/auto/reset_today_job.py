"""
A.R.K. Reset Today Job – Daily Session Hard Reset Engine.
Ensures maximum stability and disciplined session tracking.
"""

from bot.utils.session_tracker import reset_today_data
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from telegram import Bot

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

async def reset_today_job(chat_id=None, application=None):
    """
    Fully resets today's session data.
    If chat_id provided, sends user confirmation. If not, logs globally.
    """

    try:
        lang = get_language(chat_id) or "en"

        # Execute full session reset
        reset_today_data()
        logger.info(f"♻️ Daily reset successfully executed {'for user ' + str(chat_id) if chat_id else 'globally'}.")

        # If a user ID is provided, notify user
        if chat_id and application:
            bot = application.bot if application else Bot(token=config["BOT_TOKEN"])
            confirmation_message = get_text("daily_reset_success", lang) or "✅ *Today's session data has been reset successfully.*"
            await bot.send_message(chat_id=chat_id, text=confirmation_message, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ [Reset Today Job] Critical failure: {e}")
        if chat_id and application:
            bot = application.bot if application else Bot(token=config["BOT_TOKEN"])
            error_message = get_text("daily_reset_error", lang) or "❌ *Error resetting today's session.*"
            await bot.send_message(chat_id=chat_id, text=error_message, parse_mode="Markdown")
        await report_error(application.bot if application else Bot(token=config["BOT_TOKEN"]), chat_id or int(config["TELEGRAM_CHAT_ID"]), e, context_info="Reset Today Job Failure")
