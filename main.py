# bot/main.py

"""
A.R.K. – Ultra Resilient Main Entry Point.
Initialisiert den Telegram Bot, registriert alle Commands, startet alle Loops.
Made in Bali. Engineered with German Precision.
"""

import asyncio
from telegram.ext import ApplicationBuilder
from bot.handlers.commands import (
    start, help_command, analyze_symbol_handler, signal_handler,
    status_handler, uptime_handler, set_language_handler, shutdown_handler
)
from bot.handlers.global_error_handler import global_error_handler
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.startup.startup_task import execute_startup_tasks

# === Logger and Settings Setup ===
logger = setup_logger(__name__)
config = get_settings()

async def main():
    """
    Launches the complete A.R.K. Bot System.
    """
    logger.info("🚀 [Main] Launch sequence initiated...")

    # === Build Telegram Application ===
    application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()

    # === Register Core Command Handlers ===
    application.add_handler(start)
    application.add_handler(help_command)
    application.add_handler(analyze_symbol_handler)
    application.add_handler(signal_handler)
    application.add_handler(status_handler)
    application.add_handler(uptime_handler)
    application.add_handler(set_language_handler)
    application.add_handler(shutdown_handler)

    # === Register Global Error Handler ===
    application.add_error_handler(global_error_handler)

    # === Run Startup Tasks (Schedulers, Health Checks etc.) ===
    await execute_startup_tasks(application)

    # === Start Polling Loop ===
    logger.info("✅ [Main] A.R.K. Bot fully operational. Commencing live mode.")
    await application.run_polling(poll_interval=1.0)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("🛑 [Main] Manual shutdown detected. Exiting gracefully.")
