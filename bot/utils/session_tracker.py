import os
import json
import uuid
from datetime import datetime

# === Session File Location ===
SESSION_FILE = "session_data.json"

# === Internal Memory ===
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
    """Creates a new session structure."""
    return {
        "session_id": str(uuid.uuid4()),
        "start_time": datetime.utcnow().isoformat(),
        "signals_total": 0,
        "strong_signals": 0,
        "moderate_signals": 0,
        "weak_signals": 0,
        "confidence_sum": 0.0,
        "scoring_sum": 0.0,
    }

def save_session_data():
    """Saves the session data to a file."""
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(_session_data, f, indent=4)

def update_session_tracker(stars: int, confidence: float):
    """
    Updates the session tracker based on new signal data.
    Args:
        stars (int): Signal rating (1-5 stars)
        confidence (float): Confidence score (0-100%)
    """
    _session_data["signals_total"] += 1
    _session_data["confidence_sum"] += confidence

    # Weighted Scoring: 97.5% Stars + 2.5% Confidence
    weighted_score = (stars * 0.975) + ((confidence / 100) * 0.025)
    _session_data["scoring_sum"] += weighted_score

    if stars >= 4:
        _session_data["strong_signals"] += 1
    elif stars == 3:
        _session_data["moderate_signals"] += 1
    else:
        _session_data["weak_signals"] += 1

    save_session_data()

def get_session_report() -> str:
    """Returns a beautifully formatted session overview."""
    start_time = datetime.fromisoformat(_session_data["start_time"])
    uptime = datetime.utcnow() - start_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    avg_confidence = (_session_data["confidence_sum"] / _session_data["signals_total"]) if _session_data["signals_total"] > 0 else 0
    avg_scoring = (_session_data["scoring_sum"] / _session_data["signals_total"]) if _session_data["signals_total"] > 0 else 0

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
        f"*Average Confidence:* {avg_confidence:.1f}%\n"
        f"*Average Signal Quality:* {avg_scoring:.2f} (normalized)\n\n"
        f"🚀 _Session running ultra stable and precise._"
    )
    return report

def reset_session_data():
    """Resets the session data."""
    global _session_data
    _session_data = _create_new_session()
    save_session_data()
