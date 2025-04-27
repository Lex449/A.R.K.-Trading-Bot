"""
A.R.K. Daily Reset Job – Resets daily session stats.
Executed once per day at 23:59 WITA (Asia/Makassar).
"""

import logging
from bot.utils.session_tracker import reset_today_data
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

async def reset_today_job():
    """
    Performs a clean reset of today's session stats.
    """
    try:
        reset_today_data()
        logger.info("✅ Daily reset executed successfully (Today’s Data).")
    except Exception as e:
        logger.error(f"❌ Daily reset failed: {e}")
