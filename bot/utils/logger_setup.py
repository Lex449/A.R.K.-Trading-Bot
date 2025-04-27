# bot/utils/logger_setup.py

"""
A.R.K. Global Logger Setup – Premium Global Logging Initialization.
Applies unified formatting, timestamping, and silences noisy libraries cleanly.
"""

import logging
import os

def setup_global_logger():
    """
    Configures the primary global logger for the entire A.R.K. system.
    Ensures clean format, stability, and silencing of noisy external libraries.
    """
    # Create logs/ folder if missing
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    # Silence overly verbose libraries
    noisy_libraries = ["telegram", "httpx", "urllib3", "apscheduler", "aiohttp"]
    for lib in noisy_libraries:
        logging.getLogger(lib).setLevel(logging.WARNING)

    logging.info("✅ Global logger configured successfully.")
