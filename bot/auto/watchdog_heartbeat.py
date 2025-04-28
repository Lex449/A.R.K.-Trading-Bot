import time

# === Internal Heartbeat Memory ===
_last_heartbeat = time.time()

def refresh_watchdog():
    """
    Refresh the internal watchdog heartbeat.
    """
    global _last_heartbeat
    _last_heartbeat = time.time()

def get_last_heartbeat():
    """
    Returns the timestamp of the last heartbeat refresh.
    """
    return _last_heartbeat
