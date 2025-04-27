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
        "total": _empty_metrics(),
        "today": _empty_metrics(),
        "week": _empty_metrics(),
    }

def _empty_metrics():
    """Returns an empty metrics structure."""
    return {
        "signals_total": 0,
        "strong_signals": 0,
        "moderate_signals": 0,
        "weak_signals": 0,
        "confidence_sum": 0.0,
        "scoring_sum": 0.0
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
    for period in ["total", "today", "week"]:
        _session_data[period]["signals_total"] += 1
        _session_data[period]["confidence_sum"] += confidence

        weighted_score = (stars * 0.975) + ((confidence / 100) * 0.025)
        _session_data[period]["scoring_sum"] += weighted_score

        if stars >= 4:
            _session_data[period]["strong_signals"] += 1
        elif stars == 3:
            _session_data[period]["moderate_signals"] += 1
        else:
            _session_data[period]["weak_signals"] += 1

    save_session_data()

def get_session_report() -> str:
    """Returns a beautifully formatted overall session overview."""
    return _format_report("total", "📊 *Session Overview*")

def get_today_report() -> str:
    """Returns today's analysis report."""
    return _format_report("today", "🌞 *Today’s Report*")

def get_weekly_report() -> str:
    """Returns this week's analysis report."""
    return _format_report("week", "📆 *Weekly Report*")

def _format_report(section: str, title: str) -> str:
    """Helper to format any section report nicely."""
    start_time = datetime.fromisoformat(_session_data["start_time"])
    uptime = datetime.utcnow() - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    uptime_str = f"{days}d {hours}h {minutes}min" if days > 0 else f"{hours}h {minutes}min"

    data = _session_data.get(section, _empty_metrics())
    avg_confidence = (data["confidence_sum"] / data["signals_total"]) if data["signals_total"] > 0 else 0
    avg_scoring = (data["scoring_sum"] / data["signals_total"]) if data["signals_total"] > 0 else 0

    report = (
        f"{title}\n\n"
        f"*Session ID:* `{_session_data['session_id']}`\n"
        f"*Start Time:* `{start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC`\n"
        f"*Uptime:* {uptime_str}\n\n"
        f"*Total Signals:* {data['signals_total']}\n"
        f"*Strong Signals (≥4⭐):* {data['strong_signals']}\n"
        f"*Moderate Signals (3⭐):* {data['moderate_signals']}\n"
        f"*Weak Signals (≤2⭐):* {data['weak_signals']}\n"
        f"*Average Confidence:* {avg_confidence:.1f}%\n"
        f"*Average Signal Quality:* {avg_scoring:.2f} (normalized)\n\n"
        f"🚀 _Relentless progress. Relentless precision._"
    )
    return report

def reset_today_data():
    """Resets today's counters."""
    _session_data["today"] = _empty_metrics()
    save_session_data()

def reset_weekly_data():
    """Resets weekly counters."""
    _session_data["week"] = _empty_metrics()
    save_session_data()

def reset_full_session():
    """Fully resets the entire session."""
    global _session_data
    _session_data = _create_new_session()
    save_session_data()
