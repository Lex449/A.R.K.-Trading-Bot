"""
A.R.K. Session Tracker – Ultra Premium Statistics Engine 2025
Tracks signal performance, confidence levels, and rating distribution in real-time.
Built for: Transparent Recaps, Dynamic Confidence Monitoring, Institutional-Grade Reporting.
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

# === Internal Cache ===
_session_data = {}

# === Init Block ===
def initialize_session():
    """Initializes a new session or loads from disk."""
    global _session_data

    if not os.path.exists(SESSION_FILE):
        _session_data = _create_new_session()
        save_session_data()
    else:
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                _session_data = json.load(f)
                _validate_session_structure()
                logger.info("✅ [SessionTracker] Existing session loaded.")
        except Exception as e:
            logger.warning(f"⚠️ [SessionTracker] Reload failed: {e} – creating new session.")
            _session_data = _create_new_session()
            save_session_data()

def _create_new_session() -> dict:
    """Creates a new session object with default values."""
    return {
        "session_id": str(uuid.uuid4()),
        "start_time": datetime.utcnow().isoformat(),
        "signals_total": 0,
        "strong_signals": 0,
        "moderate_signals": 0,
        "weak_signals": 0,
        "total_confidence": 0.0
    }

def _validate_session_structure():
    """Ensures all required fields exist in session data."""
    required_fields = {
        "session_id": str(uuid.uuid4()),
        "start_time": datetime.utcnow().isoformat(),
        "signals_total": 0,
        "strong_signals": 0,
        "moderate_signals": 0,
        "weak_signals": 0,
        "total_confidence": 0.0
    }

    updated = False
    for key, default in required_fields.items():
        if key not in _session_data:
            _session_data[key] = default
            updated = True
            logger.warning(f"⚠️ [SessionTracker] Missing field '{key}' auto-filled.")

    if updated:
        save_session_data()

# === Runtime Functions ===
def update_session_tracker(valid_patterns_count: int, avg_confidence: float):
    """
    Updates the session with a new signal based on pattern strength and confidence.

    Args:
        valid_patterns_count (int): Number of strong patterns detected.
        avg_confidence (float): Confidence score for the signal.
    """
    try:
        _session_data["signals_total"] += 1
        _session_data["total_confidence"] += avg_confidence

        if valid_patterns_count >= 4:
            _session_data["strong_signals"] += 1
        elif valid_patterns_count == 3:
            _session_data["moderate_signals"] += 1
        else:
            _session_data["weak_signals"] += 1

        save_session_data()
        logger.info("✅ [SessionTracker] Signal recorded successfully.")

    except Exception as e:
        logger.error(f"❌ [SessionTracker] Failed to update session: {e}")

def get_session_data() -> dict:
    """
    Returns the current session data, including dynamic average.

    Returns:
        dict: Full session state.
    """
    try:
        data = _session_data.copy()
        total = data.get("signals_total", 0)
        if total > 0:
            avg_confidence = data["total_confidence"] / total
            data["avg_confidence_actual"] = round(avg_confidence, 2)
        else:
            data["avg_confidence_actual"] = 0.0
        return data

    except Exception as e:
        logger.error(f"❌ [SessionTracker] Failed to retrieve session data: {e}")
        return _create_new_session()

def save_session_data():
    """Writes session data to persistent storage."""
    try:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(_session_data, f, indent=4)
        logger.info("💾 [SessionTracker] Session saved.")
    except Exception as e:
        logger.error(f"❌ [SessionTracker] Save failed: {e}")

# === Auto Init ===
initialize_session()
