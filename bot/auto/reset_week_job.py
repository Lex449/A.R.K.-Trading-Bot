"""
A.R.K. Weekly Reset Job – Resets weekly session stats.
Executed once per week on Monday 00:00 WITA (Asia/Makassar).
"""

import logging
from bot.utils.session_tracker import reset_weekly_data
from bot.utils.logger import setup_logger

# Setup Logger
logger = setup_logger(__name__)

async def reset_week_job():
    """
    Performs a clean reset of weekly session stats.
    """
    try:
        reset_weekly_data()
        logger.info("✅ Weekly reset executed successfully (Weekly Data).")
    except Exception as e:
        logger.error(f"❌ Weekly reset failed: {e}")
