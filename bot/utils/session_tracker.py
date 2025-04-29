# bot/utils/session_tracker.py

"""
A.R.K. Session Tracker – Ultra Premium Statistics Engine 2025.
Tracks trading session performance in real-time.
"""

import os
import json
import uuid
from datetime import datetime
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === Session Data Storage ===
SESSION_FILE = "session_data.json"

# === Internal Memory ===
_session_data = {}

def initialize_session():
    """Initializes a new session or loads an existing one."""
    global _session_data

    if not os.path.exists(SESSION_FILE):
        _session_data = _create_new_session()
        save_session_data()
    else:
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                _session_data = json.load(f)
                logger.info("✅ [SessionTracker] Loaded existing session data.")
        except Exception as e:
            logger.error(f"❌ [SessionTracker] Failed to load session data: {e}")
            _session_data = _create_new_session()
            save_session_data()

def _create_new_session():
    """Creates a new session template."""
    return {
        "session_id": str(uuid.uuid4()),
        "start_time": datetime.utcnow().isoformat(),
        "signals_total": 0,
        "strong_signals": 0,
        "moderate_signals": 0,
        "weak_signals": 0,
        "total_confidence": 0.0
    }

def update_session_tracker(valid_patterns_count: int, avg_confidence: float):
    """Updates session data with a new signal."""
    try:
        _session_data["signals_total"] += valid_patterns_count
        _session_data["total_confidence"] += avg_confidence

        if valid_patterns_count >= 4:
            _session_data["strong_signals"] += 1
        elif valid_patterns_count == 3:
            _session_data["moderate_signals"] += 1
        else:
            _session_data["weak_signals"] += 1

        save_session_data()
        logger.info("✅ [SessionTracker] Updated session data.")

    except Exception as e:
        logger.error(f"❌ [SessionTracker] Failed to update session: {e}")

def get_session_data() -> dict:
    """Returns the current session statistics."""
    return _session_data

def save_session_data():
    """Saves the current session to a JSON file."""
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(_session_data, f, indent=4)
        logger.info("✅ [SessionTracker] Session data saved.")
    except Exception as e:
        logger.error(f"❌ [SessionTracker] Failed to save session data: {e}")

# === Initialize at startup ===
initialize_session()
