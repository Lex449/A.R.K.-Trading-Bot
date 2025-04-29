# bot/utils/logger.py

"""
A.R.K. Logger – Ultra Premium Structured Logging 2025.
Centralized structured logger setup for the entire bot.
"""

import logging
import os

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up and returns a structured logger instance.

    Args:
        name (str): Name of the logger (typically __name__).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        log_level = logging.DEBUG if os.getenv("ENVIRONMENT", "Production").lower() == "development" else logging.INFO
        logger.setLevel(log_level)

        console_handler = logging.StreamHandler()
        formatter = logging.Formatter("[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s", "%Y-%m-%d %H:%M:%S")
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger
