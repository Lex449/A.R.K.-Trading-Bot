# bot/analytics/performance_tracker.py

"""
Real-time performance tracker for trading signals.
Ultra-Optimized Version – Bugatti 2.0 Level
"""

import logging
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# In-Memory Performance Metrics
performance_data = {
    "total_signals": 0,
    "strong_signals": 0,
    "weak_signals": 0
}

def update_performance(stars: int):
    """
    Updates the performance statistics based on star rating.

    Args:
        stars (int): Star rating of the trade signal.
    """
    performance_data["total_signals"] += 1

    if stars >= 4:
        performance_data["strong_signals"] += 1
        logger.info(f"Strong signal recorded ({stars} stars).")
    else:
        performance_data["weak_signals"] += 1
        logger.info(f"Weak signal recorded ({stars} stars).")

def get_performance_summary() -> str:
    """
    Generates a real-time summary of trading performance.

    Returns:
        str: Formatted performance summary.
    """
    if performance_data["total_signals"] == 0:
        accuracy = 0
    else:
        accuracy = (performance_data["strong_signals"] / performance_data["total_signals"]) * 100

    return (
        f"📈 *Performance Overview*\n\n"
        f"*Total Signals:* {performance_data['total_signals']}\n"
        f"*Strong Signals (4–5⭐):* {performance_data['strong_signals']}\n"
        f"*Weak Signals (<4⭐):* {performance_data['weak_signals']}\n"
        f"*Accuracy:* {accuracy:.2f}%\n\n"
        f"⚡ _Keep managing your risk and stay sharp._"
    )
