import os
import json
from datetime import datetime

# Session file location (automatisch im Bot-Verzeichnis)
SESSION_FILE = "session_data.json"

def load_session_data():
    """Lädt bestehende Session-Daten oder initialisiert neue."""
    if not os.path.exists(SESSION_FILE):
        return {
            "start_time": datetime.utcnow().isoformat(),
            "signals_total": 0,
            "strong_signals": 0,
            "weak_signals": 0
        }

    with open(SESSION_FILE, "r") as f:
        return json.load(f)

def save_session_data(data):
    """Speichert aktuelle Session-Daten."""
    with open(SESSION_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_session_tracker(stars: int):
    """
    Aktualisiert die Session-Statistik basierend auf der Signalqualität.
    """
    data = load_session_data()

    data["signals_total"] += 1
    if stars >= 3:
        data["strong_signals"] += 1
    else:
        data["weak_signals"] += 1

    save_session_data(data)

def get_session_report() -> str:
    """
    Erzeugt eine zusammengefasste Statusmeldung zur aktuellen Trading-Session.
    """
    data = load_session_data()

    uptime = datetime.utcnow() - datetime.fromisoformat(data["start_time"])
    uptime_hours = uptime.total_seconds() // 3600
    uptime_minutes = (uptime.total_seconds() % 3600) // 60

    report = (
        f"📊 *Session Overview*\n\n"
        f"*Start Time:* `{data['start_time']}` UTC\n"
        f"*Uptime:* {int(uptime_hours)}h {int(uptime_minutes)}min\n\n"
        f"*Total Signals:* {data['signals_total']}\n"
        f"*Strong Signals (≥3⭐):* {data['strong_signals']}\n"
        f"*Weak Signals (<3⭐):* {data['weak_signals']}\n\n"
        f"🚀 _Session running smoothly._"
    )
    return report

def reset_session_data():
    """
    Setzt die Session-Daten zurück auf Null.
    Nützlich bei Neustart oder manueller Bereinigung.
    """
    save_session_data({
        "start_time": datetime.utcnow().isoformat(),
        "signals_total": 0,
        "strong_signals": 0,
        "weak_signals": 0
    })
