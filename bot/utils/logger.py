# bot/utils/logger.py

"""
Structured logger setup for all modules.
Ensures consistent, readable, and safe logging.
"""

import logging

def setup_logger(name: str) -> logging.Logger:
    """
    Initializes and returns a structured logger for a specific module.

    Args:
        name (str): Name of the module or file.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    # Prevent duplicate handlers if logger already exists
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s – %(name)s – %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False  # Prevent double logging

    logger.setLevel(logging.INFO)
    return logger
