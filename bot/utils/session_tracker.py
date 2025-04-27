# bot/utils/session_tracker.py

import os
import json
import uuid
from datetime import datetime

# Session File Location
SESSION_FILE = "session_data.json"

# Internal Memory
_session_data = {}

def initialize_session():
    """Initializes or loads the session data."""
    global _session_data

    if not os.path.exists(SESSION_FILE):
        _session_data = _create_new_session()
        save_session_data()
    else:
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                _session_data = json.load(f)
        except Exception:
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
        "total_confidence": 0.0,
    }

def save_session_data():
    """Saves the current session to a JSON file."""
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(_session_data, f, indent=4)

def update_session_tracker(stars: int, confidence: float):
    """
    Updates the session statistics based on the signal quality.
    Args:
        stars (int): Star rating (1-5)
        confidence (float): Confidence percentage (0-100)
    """
    _session_data["signals_total"] += 1
    _session_data["total_confidence"] += confidence

    if stars >= 4:
        _session_data["strong_signals"] += 1
    elif stars == 3:
        _session_data["moderate_signals"] += 1
    else:
        _session_data["weak_signals"] += 1

    save_session_data()

def get_session_report() -> str:
    """Returns a formatted overview of the current session."""
    start_time = datetime.fromisoformat(_session_data["start_time"])
    uptime = datetime.utcnow() - start_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    avg_confidence = 0.0
    if _session_data["signals_total"] > 0:
        avg_confidence = _session_data["total_confidence"] / _session_data["signals_total"]

    uptime_str = f"{days}d {hours}h {minutes}min" if days > 0 else f"{hours}h {minutes}min"

    report = (
        f"📊 *Session Overview*\n\n"
        f"*Session ID:* `{_session_data['session_id']}`\n"
        f"*Start Time:* `{start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC`\n"
        f"*Uptime:* {uptime_str}\n\n"
        f"*Total Signals:* {_session_data['signals_total']}\n"
        f"*Strong Signals (≥4⭐):* {_session_data['strong_signals']}\n"
        f"*Moderate Signals (3⭐):* {_session_data['moderate_signals']}\n"
        f"*Weak Signals (≤2⭐):* {_session_data['weak_signals']}\n"
        f"*Average Confidence:* {avg_confidence:.1f}%\n\n"
        f"🚀 _Session is running ultra stable._"
    )
    return report

def reset_session_data():
    """Resets the session statistics."""
    global _session_data
    _session_data = _create_new_session()
    save_session_data()
