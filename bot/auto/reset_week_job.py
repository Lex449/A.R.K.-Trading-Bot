"""
A.R.K. Reset Week Job – Weekly Hard Reset Engine.
Ensures maximum session hygiene and disciplined growth tracking.
"""

from bot.utils.session_tracker import reset_weekly_data
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.utils.error_reporter import report_error
from bot.config.settings import get_settings
from telegram import Bot

# Setup structured logger
logger = setup_logger(__name__)
config = get_settings()

async def reset_week_job(application, chat_id=None):
    """
    Fully resets weekly session data.
    Sends confirmation to user if chat_id provided, otherwise logs globally.
    """

    try:
        lang = get_language(chat_id) or "en"

        # Perform reset
        reset_weekly_data()
        logger.info(f"♻️ Weekly reset successfully executed {'for user ' + str(chat_id) if chat_id else 'globally'}.")

        # Confirmation
        if chat_id and application:
            bot = application.bot if application else Bot(token=config["BOT_TOKEN"])
            confirmation_message = get_text("weekly_reset_success", lang) or "✅ *This week's session data has been reset successfully.*"
            await bot.send_message(chat_id=chat_id, text=confirmation_message, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"❌ [Reset Week Job] Critical failure: {e}")
        if chat_id and application:
            bot = application.bot if application else Bot(token=config["BOT_TOKEN"])
            error_message = get_text("weekly_reset_error", lang) or "❌ *There was an error resetting the weekly session data.*"
            await bot.send_message(chat_id=chat_id, text=error_message, parse_mode="Markdown")
        await report_error(application.bot if application else Bot(token=config["BOT_TOKEN"]), chat_id or int(config["TELEGRAM_CHAT_ID"]), e, context_info="Reset Week Job Failure")
