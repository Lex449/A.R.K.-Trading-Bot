# bot/utils/session_tracker.py

import logging

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Session-wide counters
session_stats = {
    "total_signals": 0,
    "stars_3": 0,
    "stars_4": 0,
    "stars_5": 0
}

def update_session_tracker(stars: int):
    """
    Updates the session statistics based on the number of stars of the last signal.

    Args:
        stars (int): The star rating of the latest signal.
    """
    session_stats["total_signals"] += 1

    if stars == 3:
        session_stats["stars_3"] += 1
    elif stars == 4:
        session_stats["stars_4"] += 1
    elif stars == 5:
        session_stats["stars_5"] += 1

    logger.info(f"Session Update → Total: {session_stats['total_signals']}, "
                f"3⭐: {session_stats['stars_3']}, 4⭐: {session_stats['stars_4']}, 5⭐: {session_stats['stars_5']}")

def get_session_summary() -> str:
    """
    Returns a formatted session summary.

    Returns:
        str: Formatted session statistics.
    """
    return (
        f"📊 *Session Statistics*\n\n"
        f"Total Signals: {session_stats['total_signals']}\n"
        f"3-Star Signals: {session_stats['stars_3']}\n"
        f"4-Star Signals: {session_stats['stars_4']}\n"
        f"5-Star Signals: {session_stats['stars_5']}\n"
    )
