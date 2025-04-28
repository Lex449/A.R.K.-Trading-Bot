# bot/utils/session_tracker.py

"""
A.R.K. Session Tracker – Ultra Diamond Build
Tracks signals, moves, news alerts, and generates multilingual reports.
"""

import os
import json
import uuid
from datetime import datetime, timezone
from json import JSONDecodeError
from bot.utils.logger import setup_logger
from bot.utils.i18n import get_text
from bot.utils.language import get_language

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
        logger.info("📂 [Session Tracker] New session created.")
    else:
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                _session_data = json.load(f)
            logger.info("🔄 [Session Tracker] Session loaded successfully.")
        except (JSONDecodeError, Exception) as error:
            logger.warning(f"⚠️ [Session Tracker] Corrupted session detected: {error}")
            _session_data = _create_new_session()

    save_session_data()

def _create_new_session() -> dict:
    """Creates a new blank session."""
    return {
        "session_id": str(uuid.uuid4()),
        "start_time": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        "total": _empty_metrics(),
        "today": _empty_metrics(),
        "week": _empty_metrics(),
        "move_alerts": 0,
        "breaking_news_alerts": 0,
        "scans_completed": 0,
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
    """Updates session stats after every valid trading signal."""
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

def track_move_alert() -> None:
    """Tracks a detected move alert."""
    _session_data["move_alerts"] += 1
    save_session_data()

def track_breaking_news_alert() -> None:
    """Tracks a detected breaking news alert."""
    _session_data["breaking_news_alerts"] += 1
    save_session_data()

def track_scan_completed() -> None:
    """Tracks a completed scan."""
    _session_data["scans_completed"] += 1
    save_session_data()

def get_session_summary() -> dict:
    """Returns a summarized session report for internal usage."""
    if not _session_data:
        initialize_session()

    total_signals = _session_data["total"].get("signals_total", 0)
    avg_confidence = 0.0
    if total_signals > 0:
        avg_confidence = _session_data["total"].get("confidence_sum", 0.0) / total_signals

    return {
        "session_id": _session_data.get("session_id"),
        "start_time": _session_data.get("start_time"),
        "scans_completed": _session_data.get("scans_completed"),
        "signals_total": total_signals,
        "avg_confidence": round(avg_confidence, 2),
        "move_alerts": _session_data.get("move_alerts"),
        "breaking_news_alerts": _session_data.get("breaking_news_alerts"),
    }

def _format_report(section: str, title: str) -> str:
    """Formats a detailed human-readable session report."""
    start_time = datetime.fromisoformat(_session_data.get("start_time"))
    uptime = datetime.utcnow() - start_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    uptime_str = f"{days}d {hours}h {minutes}m" if days else f"{hours}h {minutes}m"

    data = _session_data.get(section, _empty_metrics())
    avg_conf = (data["confidence_sum"] / data["signals_total"]) if data["signals_total"] else 0
    avg_score = (data["scoring_sum"] / data["signals_total"]) if data["signals_total"] else 0

    lang = get_language()

    report = (
        f"{title}\n\n"
        f"*{get_text('session_id', lang)}:* `{_session_data['session_id']}`\n"
        f"*{get_text('start_time', lang)}:* `{start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC`\n"
        f"*{get_text('uptime', lang)}:* {uptime_str}\n\n"
        f"*{get_text('total_signals', lang)}:* {data['signals_total']}\n"
        f"*{get_text('strong_signals', lang)}:* {data['strong_signals']}\n"
        f"*{get_text('moderate_signals', lang)}:* {data['moderate_signals']}\n"
        f"*{get_text('weak_signals', lang)}:* {data['weak_signals']}\n"
        f"*{get_text('avg_confidence', lang)}:* `{avg_conf:.1f}%`\n"
        f"*{get_text('avg_score', lang)}:* `{avg_score:.2f}`\n\n"
        f"🚀 _{get_text('relentless_footer', lang)}_"
    )
    return report

def get_session_report(chat_id: int = None) -> str:
    """Returns the full session overview."""
    return _format_report("total", get_text("session_title_total", get_language(chat_id)))

def get_today_report(chat_id: int = None) -> str:
    """Returns today's trading performance."""
    return _format_report("today", get_text("session_title_today", get_language(chat_id)))

def get_weekly_report(chat_id: int = None) -> str:
    """Returns weekly trading performance."""
    return _format_report("week", get_text("session_title_week", get_language(chat_id)))

def reset_today_data() -> None:
    """Resets today's stats."""
    _session_data["today"] = _empty_metrics()
    save_session_data()

def reset_weekly_data() -> None:
    """Resets this week's stats."""
    _session_data["week"] = _empty_metrics()
    save_session_data()

def reset_full_session() -> None:
    """Completely resets session tracker."""
    global _session_data
    _session_data = _create_new_session()
    save_session_data()
