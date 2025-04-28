"""
A.R.K. Reset Today Job – Daily Session Reset.
Executed once per day (user timezone controlled).
"""

from bot.utils.session_tracker import reset_today_data
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language

# Setup structured logger
logger = setup_logger(__name__)

async def reset_today_job(chat_id=None):
    """
    Resets today's session data.
    Optional chat_id for logging context.
    """
    try:
        # Fetch user language preference
        lang = get_language(chat_id) or "en"

        # Execute the reset
        reset_today_data()
        
        # Notify user in their language
        confirmation_message = get_text("daily_reset_success", lang) or "✅ *Today's session data has been reset successfully.*"

        if chat_id:
            await chat_id.reply_text(confirmation_message, parse_mode="Markdown")
            logger.info(f"♻️ Daily reset executed for user: {chat_id}")
        else:
            logger.info("♻️ Daily reset executed globally.")

    except Exception as e:
        logger.error(f"❌ Daily reset failed: {e}")
        # Send error notification if needed
        error_message = get_text("daily_reset_error", lang) or "❌ *There was an error resetting today's session.*"
        if chat_id:
            await chat_id.reply_text(error_message, parse_mode="Markdown")
