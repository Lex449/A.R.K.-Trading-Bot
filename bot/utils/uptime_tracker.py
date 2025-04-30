"""
A.R.K. Uptime Tracker – NASA-Level Stability Module 2025
Tracks system uptime with ultra-high precision and human-readable output.
Made in Bali. Engineered with German Precision.
"""

import time
from datetime import timedelta

# Capture launch timestamp once at bot startup
_start_time = time.monotonic()

def get_uptime() -> str:
    """
    Calculates and returns the formatted uptime since bot initialization.

    Returns:
        str: Uptime in a clean human-readable format.
    """

    elapsed_seconds = int(time.monotonic() - _start_time)
    uptime = str(timedelta(seconds=elapsed_seconds))

    # Parse result to display cleaner for < 1 day or < 1 hour
    if "day" in uptime or "days" in uptime:
        return uptime  # e.g., '1 day, 2:45:33'
    elif elapsed_seconds < 3600:
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        return f"{minutes}m {seconds}s"
    else:
        return uptime  # e.g., '2:45:33'
