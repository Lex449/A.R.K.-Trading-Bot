"""
A.R.K. Reset Week Job – Weekly Session Reset.
Executed once per week (user timezone controlled).
"""

from bot.utils.session_tracker import reset_weekly_data
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def reset_week_job(chat_id=None):
    """
    Resets weekly session data.
    Optional chat_id for logging context.
    """
    try:
        reset_weekly_data()
        if chat_id:
            logger.info(f"♻️ Weekly reset executed for user: {chat_id}")
        else:
            logger.info("♻️ Weekly reset executed globally.")
    except Exception as e:
        logger.error(f"❌ Weekly reset failed: {e}")
