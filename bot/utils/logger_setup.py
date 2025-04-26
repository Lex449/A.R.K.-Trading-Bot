# bot/utils/logger_setup.py

import logging

def setup_logger():
    """
    Configures a centralized logger for the entire bot system
    with enhanced formatting, timestamps, and colored console output.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="\n[%(asctime)s] | %(levelname)s | %(name)s: %(message)s\n",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Reduce noise from external libraries
    logging.getLogger("telegram").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
