# bot/utils/logger_setup.py

import logging
import sys

def setup_logger():
    """
    Sets up an enhanced logger for the A.R.K. Trading Bot.
    Outputs to console in a clean, formatted way.
    """

    # Logger holen
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Log-Format
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # StreamHandler für Konsole
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Alte Handler entfernen (falls doppelt)
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(console_handler)

    # Bestätigung
    logger.info("✅ Logging system initialized successfully.")
