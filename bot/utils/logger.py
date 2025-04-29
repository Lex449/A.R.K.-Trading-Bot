# bot/utils/logger.py

"""
A.R.K. Logger – Structured Precision Logging 2025
Maximale Stabilität und Transparenz für alle Module.
"""

import logging
import os

def setup_logger(name: str = "A.R.K. Logger") -> logging.Logger:
    """
    Creates and returns a structured logger for the given module name.
    Logs to console and (optionally) to a file if in production mode.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicated handlers
    if logger.handlers:
        return logger

    # Console Handler
    console_handler = logging.StreamHandler()
    console_format = logging.Formatter("[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # Optional: Log to file if environment is Production
    environment = os.getenv("ENVIRONMENT", "Development")
    if environment == "Production":
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(log_dir, "bot.log"), encoding="utf-8")
        file_format = logging.Formatter("[%(asctime)s] %(levelname)-8s | %(name)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger
