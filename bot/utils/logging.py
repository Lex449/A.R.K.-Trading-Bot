# bot/utils/logging.py

"""
Premium Logger Setup for A.R.K. Trading Bot.
Ensures structured console output with timestamps and module names.
"""

import logging
import sys

def setup_logger():
    """
    Configures a centralized, clean, and powerful logger for the entire system.
    Avoids double handlers and ensures perfect output formatting.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # StreamHandler → Konsole (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Doppelte Handler verhindern (wichtig für Replit, Railway etc.)
    if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
        logger.addHandler(console_handler)

    # Clean Info-Ausgabe für Bestätigung
    logger.info("✅ Logger initialized successfully for A.R.K. Bot.")

    return logger
