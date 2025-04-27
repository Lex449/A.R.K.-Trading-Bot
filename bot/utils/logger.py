# bot/utils/logger.py

"""
A.R.K. Ultra Logger – Premium Structured Logging.
Optimized for scaling, stability, and clean dev/prod operations.
"""

import logging
import sys

def setup_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Creates a structured, production-grade logger.

    Args:
        name (str): Name of the module.
        level (str): Logging level ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL").

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Stream Handler for console output
        stream_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        stream_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
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
