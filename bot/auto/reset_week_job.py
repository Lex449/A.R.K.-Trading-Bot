"""
A.R.K. Reset Week Job – Weekly Session Reset.
Executed once per week (user timezone controlled).
"""

from bot.utils.session_tracker import reset_weekly_data
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language
from bot.utils.error_reporter import report_error

# Setup structured logger
logger = setup_logger(__name__)

async def reset_week_job(application, chat_id=None):
    """
    Resets weekly session data.
    Optional chat_id for logging context.
    """
    try:
        # Determine user language
        lang = get_language(chat_id) or "en"

        # Perform weekly reset
        reset_weekly_data()

        # Retrieve confirmation text
        confirmation_message = get_text("weekly_reset_success", lang) or (
            "♻️ Weekly session reset completed successfully!"
        )

        if chat_id:
            await application.bot.send_message(
                chat_id=chat_id,
                text=confirmation_message,
                parse_mode="Markdown"
            )
            logger.info(f"♻️ Weekly reset executed for user: {chat_id}")
        else:
            logger.info("♻️ Weekly reset executed globally.")

    except Exception as e:
        await report_error(application.bot, chat_id, e, context_info="Weekly Reset Job")
        logger.error(f"❌ Weekly reset failed: {e}")
