# bot/auto/watchdog_state.py

"""
A.R.K. Watchdog Heartbeat State – Standalone Module.
Handles heartbeat timestamps for monitoring.
"""

import time

# Global heartbeat timestamp
_last_heartbeat = time.time()

def refresh_watchdog():
    """
    Refreshes the global heartbeat timestamp.
    This function updates the last known heartbeat time to the current time.
    """
    global _last_heartbeat
    _last_heartbeat = time.time()

def get_last_heartbeat():
    """
    Returns the last heartbeat timestamp.
    This function is used to monitor the time since the last known heartbeat.
    """
    return _last_heartbeat
