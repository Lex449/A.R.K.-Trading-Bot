"""
Central logger configuration for the entire bot.
Applies clean formatting, timestamping, and suppresses unnecessary noise.
"""

import logging

def setup_logger():
    """
    Configures a global logger for the entire A.R.K. system.
    Provides uniform log formatting and reduces noise from external libraries.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="\n[%(asctime)s] | %(levelname)s | %(name)s | %(message)s\n",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Reduce verbosity from noisy third-party libraries
    for noisy_logger in ["telegram", "httpx", "urllib3", "apscheduler"]:
        logging.getLogger(noisy_logger).setLevel(logging.WARNING)
