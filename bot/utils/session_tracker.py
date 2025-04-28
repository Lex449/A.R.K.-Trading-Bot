# bot/utils/session_tracker.py

"""
A.R.K. Session Tracker – Ultra Stable Build.
Tracks session, daily, and weekly trading performance.
"""

import os
import json
import uuid
from datetime import datetime
from json import JSONDecodeError
from bot.utils.logger import setup_logger

# Setup structured logger
logger = setup_logger(__name__)

# === File Location ===
SESSION_FILE = "session_data.json"

# === Internal Memory ===
_session_data = {}

def initialize_session() -> None:
    """Initializes or loads session data."""
    global _session_data

    if not os.path.exists(SESSION_FILE):
        _session_data = _create_new_session()
        logger.info("📂 [Session Tracker] New session file created.")
    else:
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                _session_data = json.load(f)
        except (JSONDecodeError, Exception) as error:
            logger.warning(f"⚠️ [Session Tracker] Corrupted session file detected: {error}")
            _session_data = _create_new_session()

    save_session_data()

def _create_new_session() -> dict:
    """Creates a new blank session."""
    return {
        "session_id": str(uuid.uuid4()),
        "start_time": datetime.utcnow().isoformat(),
        "total": _empty_metrics(),
        "today": _empty_metrics(),
        "week": _empty_metrics(),
    }

def _empty_metrics() -> dict:
    """Returns a blank metric structure."""
    return {
        "signals_total": 0,
        "strong_signals": 0,
        "moderate_signals": 0,
        "weak_signals": 0,
        "confidence_sum": 0.0,
        "scoring_sum": 0.0,
    }

def save_session_data() -> None:
    """Saves the current session data to file."""
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        json.dump(_session_data, f, indent=4)

def update_session_tracker(stars: int, confidence: float) -> None:
    """Updates session statistics after every signal."""
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
    """Returns full session overview."""
    return _format_report("total", "📊 *Session Overview*")

def get_today_report() -> str:
    """Returns today's performance report."""
    return _format_report("today", "🌞 *Today’s Report*")

def get_weekly_report() -> str:
    """Returns this week's performance report."""
    return _format_report("week", "📆 *Weekly Report*")

def _format_report(section: str, title: str) -> str:
    """Formats the session data into a readable message."""
    start_time = datetime.fromisoformat(_session_data.get("start_time"))
    uptime = datetime.utcnow() - start_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    uptime_str = f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"

    data = _session_data.get(section, _empty_metrics())
    avg_confidence = (data["confidence_sum"] / data["signals_total"]) if data["signals_total"] else 0
    avg_scoring = (data["scoring_sum"] / data["signals_total"]) if data["signals_total"] else 0

    report = (
        f"{title}\n\n"
        f"*Session ID:* `{_session_data['session_id']}`\n"
        f"*Start Time:* `{start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC`\n"
        f"*Uptime:* {uptime_str}\n\n"
        f"*Total Signals:* {data['signals_total']}\n"
        f"*Strong Signals (≥4⭐):* {data['strong_signals']}\n"
        f"*Moderate Signals (3⭐):* {data['moderate_signals']}\n"
        f"*Weak Signals (≤2⭐):* {data['weak_signals']}\n"
        f"*Avg Confidence:* `{avg_confidence:.1f}%`\n"
        f"*Avg Signal Score:* `{avg_scoring:.2f}`\n\n"
        f"🚀 _Relentless progress. Relentless precision._"
    )
    return report

def reset_today_data() -> None:
    """Resets today's performance data."""
    _session_data["today"] = _empty_metrics()
    save_session_data()

def reset_weekly_data() -> None:
    """Resets weekly performance data."""
    _session_data["week"] = _empty_metrics()
    save_session_data()

def reset_full_session() -> None:
    """Resets the entire session."""
    global _session_data
    _session_data = _create_new_session()
    save_session_data()
