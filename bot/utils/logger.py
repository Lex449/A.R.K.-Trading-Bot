# bot/utils/logger.py

"""
A.R.K. Ultra Logger – Production Grade Structured Logging.
Designed for scaling, monitoring, and surgical debugging.
"""

import logging
import sys
import os
from logging.handlers import TimedRotatingFileHandler

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Creates a fully structured, premium logger for modules.

    Args:
        name (str): Module or context name.
        level (str): Logging level.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Create logs/ folder if missing
        os.makedirs("logs", exist_ok=True)

        # StreamHandler (Console Output)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        stream_handler.setFormatter(stream_formatter)

        # FileHandler (Daily rotating logs)
        file_handler = TimedRotatingFileHandler(
            filename="logs/ark_bot.log",
            when="midnight",
            interval=1,
            backupCount=7,  # Keep last 7 days
            encoding="utf-8"
        )
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # Add both handlers
        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        logger.propagate = False  # Avoid duplicate logs

    # Set Logging Level
    level_mapping = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    logger.setLevel(level_mapping.get(level.upper(), logging.INFO))

    return logger
