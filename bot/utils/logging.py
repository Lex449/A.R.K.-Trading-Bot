# bot/utils/logging.py

import logging
import os
import sys

def setup_logger():
    """
    Configures a premium-grade logger for A.R.K. Bot.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[%(asctime)s] | %(levelname)s | %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(console_handler)

    # Optional: Print Environment (Production/Development)
    env = os.getenv("ENVIRONMENT", "Production").capitalize()
    logger.info(f"✅ Logger initialized successfully for A.R.K. Bot (Environment: {env})")

    return logger
