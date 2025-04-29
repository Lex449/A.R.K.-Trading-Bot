# bot/main.py

"""
A.R.K. – Ultra Resilient Main Entry Point.
Initialisiert den Telegram Bot, registriert alle Commands, startet alle Loops.
Made in Bali. Engineered with German Precision.
"""

import asyncio
import logging
from telegram.ext import ApplicationBuilder
from bot.handlers.commands import (
    start, help_command, analyze_symbol_handler, signal_handler,
    status_handler, uptime_handler, set_language_handler, shutdown_handler
)
from bot.handlers.global_error_handler import global_error_handler
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.startup.startup_task import execute_startup_tasks

# Setup logger
logger = setup_logger(__name__)
config = get_settings()

async def main():
    """
    A.R.K. Bot Initializer
    """
    logger.info("🚀 A.R.K. is preparing for launch...")

    # Application Build
    application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()

    # === Command Handlers ===
    application.add_handler(start)
    application.add_handler(help_command)
    application.add_handler(analyze_symbol_handler)
    application.add_handler(signal_handler)
    application.add_handler(status_handler)
    application.add_handler(uptime_handler)
    application.add_handler(set_language_handler)
    application.add_handler(shutdown_handler)

    # === Error Handler ===
    application.add_error_handler(global_error_handler)

    # === Startup Tasks (Scheduler + Commands) ===
    await execute_startup_tasks(application)

    # === Start Polling ===
    logger.info("✅ A.R.K. initialized successfully. Launching into action.")
    await application.run_polling()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.warning("🛑 A.R.K. shutdown initiated manually.")
