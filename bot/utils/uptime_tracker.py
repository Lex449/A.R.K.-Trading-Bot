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
        str: Uptime in the format "X days, HH:MM:SS"
    """

    elapsed_seconds = int(time.monotonic() - _start_time)
    uptime_duration = str(timedelta(seconds=elapsed_seconds))

    # Dynamic formatting: If <1 day, hide "0 days"
    if uptime_duration.startswith("0:"):
        hours_minutes_seconds = uptime_duration.split(", ")[-1]
        return hours_minutes_seconds

    return uptime_duration
