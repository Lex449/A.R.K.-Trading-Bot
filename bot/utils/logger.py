# bot/utils/logger.py

"""
A.R.K. Logger Setup – Structured Ultra Premium Logging 2025.
Provides consistent, structured, and readable logging across the bot.
"""

import logging
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Creates a standardized logger instance for modules.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Clear any existing handlers (avoid duplicates)
    if logger.hasHandlers():
        logger.handlers.clear()

    # Setup StreamHandler
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="[{asctime}] [{levelname}] {name}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
