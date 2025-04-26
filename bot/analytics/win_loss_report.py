# bot/analytics/win_loss_report.py

"""
Generates win/loss reports for trading session reviews.
Ultra-Optimized Version – Bugatti 2.0 Level
"""

from datetime import datetime
from bot.analytics.performance_tracker import get_performance_summary
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

def generate_win_loss_report() -> str:
    """
    Compiles a detailed win/loss performance report.

    Returns:
        str: Formatted win/loss report for session overview.
    """
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    performance = get_performance_summary()

    logger.info(f"Generated Win/Loss report at {now}.")

    return (
        f"📊 *Win/Loss Report*\n"
        f"🕒 *Generated:* `{now}`\n\n"
        f"{performance}\n"
        f"🧠 _Stay focused, improve daily._"
    )
