# bot/utils/logging.py

"""
A.R.K. System Logger – Premium Setup for Ultra Clean Console Outputs.
Optimized for production environments and structured monitoring.
"""

import logging
import os
import sys

def setup_logger():
    """
    Configures the global A.R.K. system logger for consistent output.
    Console output only, fully formatted, ready for production use.
    """

    # Create base logger
    logger = logging.getLogger()

    # === Clean Setup: Prevent duplicate handlers ===
    if not logger.hasHandlers():
        # Set StreamHandler (stdout)
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = logging.Formatter(
            "[%(asctime)s] | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    logger.setLevel(logging.INFO)

    # === Startup Message with Environment Context ===
    env = os.getenv("ENVIRONMENT", "Production").capitalize()
    logger.info(f"✅ [Logger Setup] A.R.K. Logger initialized successfully (Environment: {env})")

    return logger
