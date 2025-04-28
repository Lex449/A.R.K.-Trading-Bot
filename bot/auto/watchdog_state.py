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
    """
    global _last_heartbeat
    _last_heartbeat = time.time()

def get_last_heartbeat():
    """
    Returns the last heartbeat timestamp.
    """
    return _last_heartbeat
