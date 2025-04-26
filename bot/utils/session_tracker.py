import os
import json
from datetime import datetime, timedelta
import uuid

# Session file location
SESSION_FILE = "session_data.json"

# Internal memory (keine ständige Datei-Lese)
_session_data = {}

def initialize_session():
    """Initialisiert oder lädt bestehende Session-Daten."""
    global _session_data

    if not os.path.exists(SESSION_FILE):
        _session_data = {
            "session_id": str(uuid.uuid4()),
            "start_time": datetime.utcnow().isoformat(),
            "signals_total": 0,
            "strong_signals": 0,
            "weak_signals": 0,
            "star_sum": 0
        }
        save_session_data()
    else:
        try:
            with open(SESSION_FILE, "r") as f:
                _session_data = json.load(f)
        except Exception:
            # Bei korruptem JSON neu starten
            _session_data = {
                "session_id": str(uuid.uuid4()),
                "start_time": datetime.utcnow().isoformat(),
                "signals_total": 0,
                "strong_signals": 0,
                "weak_signals": 0,
                "star_sum": 0
            }
            save_session_data()

def save_session_data():
    """Speichert die aktuelle Session."""
    with open(SESSION_FILE, "w") as f:
        json.dump(_session_data, f, indent=4)

def update_session_tracker(stars: int):
    """
    Aktualisiert die Session-Statistik basierend auf der Signalqualität.
    """
    _session_data["signals_total"] += 1
    _session_data["star_sum"] += stars

    if stars >= 3:
        _session_data["strong_signals"] += 1
    else:
        _session_data["weak_signals"] += 1

    save_session_data()

def get_session_report() -> str:
    """
    Gibt eine formattierte Übersicht der aktuellen Session zurück.
    """
    start_time = datetime.fromisoformat(_session_data["start_time"])
    uptime = datetime.utcnow() - start_time

    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    average_stars = 0
    if _session_data["signals_total"] > 0:
        average_stars = round(_session_data["star_sum"] / _session_data["signals_total"], 2)

    uptime_str = ""
    if days > 0:
        uptime_str += f"{days}d "
    uptime_str += f"{hours}h {minutes}min"

    report = (
        f"📊 *Session Overview*\n\n"
        f"*Session ID:* `{_session_data['session_id']}`\n"
        f"*Start Time:* `{_session_data['start_time']}` UTC\n"
        f"*Uptime:* {uptime_str}\n\n"
        f"*Total Signals:* {_session_data['signals_total']}\n"
        f"*Strong Signals (≥3⭐):* {_session_data['strong_signals']}\n"
        f"*Weak Signals (<3⭐):* {_session_data['weak_signals']}\n"
        f"*Average Signal Quality:* {average_stars} ⭐\n\n"
        f"🚀 _Session running ultra stable._"
    )
    return report

def reset_session_data():
    """
    Setzt die Session-Daten zurück auf Null und erstellt neue Session-ID.
    """
    global _session_data
    _session_data = {
        "session_id": str(uuid.uuid4()),
        "start_time": datetime.utcnow().isoformat(),
        "signals_total": 0,
        "strong_signals": 0,
        "weak_signals": 0,
        "star_sum": 0
    }
    save_session_data()
