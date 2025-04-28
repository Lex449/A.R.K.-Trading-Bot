# bot/auto/watchdog_heartbeat.py

import time

# === Internal Heartbeat Memory ===
_last_heartbeat = time.time()

def refresh_watchdog():
    """
    Refresh the internal watchdog heartbeat.
    Updates the timestamp of the last heartbeat to the current time.
    """
    global _last_heartbeat
    _last_heartbeat = time.time()

def get_last_heartbeat():
    """
    Returns the timestamp of the last heartbeat refresh.
    This is used to track the time since the last successful operation.
    """
    return _last_heartbeat
