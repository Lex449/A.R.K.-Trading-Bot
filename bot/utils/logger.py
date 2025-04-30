"""
A.R.K. Logger – Ultra Premium Structured Logging 2025
Centralized structured logger setup with dynamic environment awareness.

Built for: Consistency, Clarity, Cross-System Debugging.
Made in Bali. Engineered with German Precision.
"""

import logging
import os
import sys

def setup_logger(name: str) -> logging.Logger:
    """
    Sets up and returns a structured logger instance.

    Args:
        name (str): Name of the logger (usually __name__).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        # Environment-based logging level
        env = os.getenv("ENVIRONMENT", "production").lower()
        level = logging.DEBUG if env in ("dev", "development") else logging.INFO
        logger.setLevel(level)

        # Stream handler (stdout)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            "[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        ))

        logger.addHandler(handler)
        logger.propagate = False  # Prevent double logging in some environments

    return logger
