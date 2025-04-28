# bot/utils/logger_setup.py

"""
A.R.K. Global Logger Setup – Premium Global Logging Initialization.
Applies unified formatting, timestamping, and silences noisy libraries cleanly.
"""

import logging
import os

def setup_global_logger(level: str = "INFO"):
    """
    Configures the primary global logger for the entire A.R.K. system.
    Ensures clean format, stability, and silencing of noisy external libraries.

    Args:
        level (str): Desired logging level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").
    """
    # Create logs/ folder if missing
    os.makedirs("logs", exist_ok=True)

    level_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    resolved_level = level_mapping.get(level.upper(), logging.INFO)

    logging.basicConfig(
        level=resolved_level,
        format='[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    # Silence overly verbose libraries
    noisy_libraries = ["telegram", "httpx", "urllib3", "apscheduler", "aiohttp"]
    for lib in noisy_libraries:
        logging.getLogger(lib).setLevel(logging.WARNING)

    logging.info(f"✅ [Logger Setup] Global logger configured successfully at level: {level.upper()}")
