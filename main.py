# main.py

"""
A.R.K. – Ultra Resilient Main Entry Point.
Initialisiert den Telegram Bot, registriert alle Commands, startet alle Loops.
Made in Bali. Engineered with German Precision.
"""

import asyncio
import nest_asyncio
from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers.commands import (
    start,
    help_command,
    analyze_symbol_handler,
    signal_handler,
    status_handler,
    uptime_handler,
    set_language_handler,
    shutdown_handler,
    monitor_handler  # ✅ NEU
)
from bot.handlers.global_error_handler import global_error_handler
from bot.config.settings import get_settings
from bot.utils.logger import setup_logger
from bot.utils.usage_monitor import start_usage_monitor_loop  # ✅ NEU
from bot.startup.startup_task import execute_startup_tasks

# === Logger & Settings Setup ===
logger = setup_logger(__name__)
config = get_settings()

# === Railway Compatibility Patch ===
nest_asyncio.apply()

async def main():
    """
    Launches the complete A.R.K. Bot System.
    """
    logger.info("🚀 [Main] Launch sequence initiated...")

    try:
        # === Build Telegram Application ===
        application = ApplicationBuilder().token(config["BOT_TOKEN"]).build()

        # === Register Command Handlers ===
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("analyse", analyze_symbol_handler))
        application.add_handler(CommandHandler("signal", signal_handler))
        application.add_handler(CommandHandler("status", status_handler))
        application.add_handler(CommandHandler("uptime", uptime_handler))
        application.add_handler(CommandHandler("setlanguage", set_language_handler))
        application.add_handler(CommandHandler("shutdown", shutdown_handler))
        application.add_handler(CommandHandler("monitor", monitor_handler))  # ✅ NEU

        # === Register Global Error Handler ===
        application.add_error_handler(global_error_handler)

        # === Start Internal Usage Monitor Loop ===
        asyncio.create_task(start_usage_monitor_loop(application))  # ✅ NEU

        # === Run Startup Pipeline ===
        await execute_startup_tasks(application)

        # === Start Polling Loop ===
        logger.info("✅ [Main] A.R.K. Bot fully operational. Commencing live mode.")
        await application.run_polling(poll_interval=1.0)

    except Exception as e:
        logger.critical(f"🔥 [Main] Critical Startup Failure: {e}")
        raise

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
