# bot/utils/session_tracker.py

"""
Handles session tracking for signals, uptime, and statistics.
Built for high-performance bots.
"""

import os
import json
import uuid
from datetime import datetime
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# Session file location
SESSION_FILE = "session_data.json"

# Internal memory (no constant file reading)
_session_data = {}

def initialize_session():
    """Initializes or loads session data from file."""
    global _session_data

    if not os.path.exists(SESSION_FILE):
        logger.warning("No existing session data found. Creating new session.")
        _session_data = _new_session()
        save_session_data()
    else:
        try:
            with open(SESSION_FILE, "r") as f:
                _session_data = json.load(f)
                logger.info(f"Loaded existing session: ID {_session_data.get('session_id', 'unknown')}")
        except Exception as e:
            logger.error(f"Failed to load session file, starting new. Error: {e}")
            _session_data = _new_session()
            save_session_data()

def _new_session() -> dict:
    """Generates a fresh new session structure."""
    return {
        "session_id": str(uuid.uuid4()),
        "start_time": datetime.utcnow().isoformat(),
        "signals_total": 0,
        "strong_signals": 0,
        "weak_signals": 0,
        "star_sum": 0
    }

def save_session_data():
    """Saves session data to file."""
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(_session_data, f, indent=4)
        logger.debug("Session data saved successfully.")
    except Exception as e:
        logger.error(f"Error saving session data: {e}")

def update_session_tracker(stars: int):
    """
    Updates the session statistics based on signal strength.

    Args:
        stars (int): Star rating (1–5) of the signal.
    """
    _session_data["signals_total"] += 1
    _session_data["star_sum"] += stars

    if stars >= 3:
        _session_data["strong_signals"] += 1
    else:
        _session_data["weak_signals"] += 1

    logger.debug(f"Session updated: Total={_session_data['signals_total']}, Stars={stars}")
    save_session_data()

def get_session_report() -> str:
    """
    Generates a human-readable session report.

    Returns:
        str: Session status report.
    """
    start_time = datetime.fromisoformat(_session_data["start_time"])
    uptime = datetime.utcnow() - start_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    average_stars = round(_session_data["star_sum"] / _session_data["signals_total"], 2) if _session_data["signals_total"] else 0

    uptime_str = ""
    if days > 0:
        uptime_str += f"{days}d "
    uptime_str += f"{hours}h {minutes}min"

    return (
        f"📊 *Session Overview*\n\n"
        f"*Session ID:* `{_session_data['session_id']}`\n"
        f"*Start Time:* `{_session_data['start_time']}` UTC\n"
        f"*Uptime:* {uptime_str}\n\n"
        f"*Total Signals:* {_session_data['signals_total']}\n"
        f"*Strong Signals (≥3⭐):* {_session_data['strong_signals']}\n"
        f"*Weak Signals (<3⭐):* {_session_data['weak_signals']}\n"
        f"*Avg Quality:* {average_stars} ⭐\n\n"
        f"🛡️ _Session stable and monitored._"
    )

def reset_session_data():
    """Resets session statistics and creates a new session ID."""
    global _session_data
    logger.warning("Session reset triggered. Starting new session.")
    _session_data = _new_session()
    save_session_data()
