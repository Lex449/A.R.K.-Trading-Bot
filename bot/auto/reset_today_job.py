"""
A.R.K. Reset Today Job – Daily Session Reset.
Executed once per day (user timezone controlled).
"""

from bot.utils.session_tracker import reset_today_data
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

async def reset_today_job(chat_id=None):
    """
    Resets today's session data.
    Optional chat_id for logging context.
    """
    try:
        reset_today_data()
        if chat_id:
            logger.info(f"♻️ Daily reset executed for user: {chat_id}")
        else:
            logger.info("♻️ Daily reset executed globally.")
    except Exception as e:
        logger.error(f"❌ Daily reset failed: {e}")
